#!/usr/bin/python2.7

"""
# cms_functions.py
# Author: Christopher Treadgold
# Date: N/D
# Edited: 07/08/2016 | Christopher Treadgold
"""

import json
import mimetypes
import os
import sys
import time
import uuid
import zipfile
from io import BytesIO

import boto3
import botocore
import apigatewaysetup

from replace_variables import replace_variables


class AwsFunc:
    """ Contains functions for creating, modifying and deleting elements of the
    AWSCMS. Requires awscli configured or an aws configuration file.
    """

    def __init__(self, cms_prefix, region="us-east-1"):
        """ Gets low-level clients for services to be used and creates
        containers for AWS objects that will be filled by creation functions.
        """
        self.region = region
        self.constants = {}
        self.cms_prefix = cms_prefix
        with open("postfixes.json", "r") as postfixes_file:
            postfixes = json.loads(postfixes_file.read())
        for key in postfixes.keys():
            self.constants[key] = unicode(cms_prefix, "utf-8") + postfixes[key]

        self.constants["DISQUS-ID"] = "arc-cms"

    def upload_file(self, path, key):
        """ Uploads a file to s3 """
        # Prepare argument variables
        bucket_name = self.constants["BUCKET"]
        put_kwargs = {}
        mime = mimetypes.guess_type(path)
        if mime[0] != None:
            put_kwargs["ContentType"] = mime[0]
        if mime[1] != None:
            put_kwargs["ContentEncoding"] = mime[1]

        # Store file data and make replacements to files with certain mimetypes
        with open(path, "rb") as file_body:
            body = file_body.read()
        if type(mime[0]) is str and not mime[0].startswith("image/"):
            body = replace_variables(body, **self.constants)
        put_kwargs.update({
            "Bucket": bucket_name,
            "ACL": "public-read",
            "Body": body,
            "Key": key
        })

        # Upload file to s3
        try:
            print "Uploading: %s" % key
            s3 = boto3.client("s3")
            s3.put_object(**put_kwargs)
            print "Complete"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def create_bucket(self):
        """ Creates a bucket in region "bucket_region".
        
        If "bucket_region" is not given, bucket will default to US Standard
        region. Files for the AWS CMS are uploaded to the bucket.
        """
        bucket_name = self.constants["BUCKET"]
        bucket_kwargs = {"ACL": "public-read", "Bucket": bucket_name}
        if self.region != "us-east-1":
            bucket_kwargs["CreateBucketConfiguration"] = {
                "LocationConstraint": self.region}

        # Create bucket
        try:
            s3 = boto3.client("s3")
            print "Creating bucket: %s" % (bucket_name)
            bucket = s3.create_bucket(**bucket_kwargs)
            print "Bucket created"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

        # add bucket CORS
        try:
            s3 = boto3.client("s3")
            s3.put_bucket_cors(
                Bucket=bucket_name,
                CORSConfiguration={
                    "CORSRules": [{
                        "AllowedOrigins": ["*"],
                        "AllowedMethods": ["GET", "POST"],
                        "AllowedHeaders": ["Authorization", "Cache-Control",
                                           "Upgrade-Insecure-Requests"],
                        "MaxAgeSeconds": 3000
                    }]
                }
            )
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

        # Populate the bucket, adding all files from the website folder
        print "Populating bucket"
        for root, dirs, files in os.walk("website"):
            for fl in files:
                path = os.path.join(root, fl)
                key = path[8:]
                # If the file has backslashes in it, replace them with forwardslashes
                key = key.replace("\\", "/")
                self.upload_file(path, key)
        print "Bucket populated"

    def create_cloudfront_distribution(self):
        """ Creates a coudfront distribution linked to the s3 bucket """
        try:
            print "Creating cloudfront distribution"
            origin_id = str(uuid.uuid4())
            cloudfront = boto3.client("cloudfront")
            cloudfront.create_distribution(
                DistributionConfig={
                    "CallerReference": str(uuid.uuid4()),
                    "DefaultRootObject": "index.html",
                    "Origins": {
                        "Quantity": 1,
                        "Items": [
                            {
                                "Id": origin_id,
                                "DomainName": "%s.s3.amazonaws.com" % (
                                    self.constants["BUCKET"]),
                                "S3OriginConfig": {
                                    "OriginAccessIdentity": ""
                                }
                            }
                        ]
                    },
                    "DefaultCacheBehavior": {
                        "TargetOriginId": origin_id,
                        "ForwardedValues": {
                            "QueryString": False,
                            "Cookies": {
                                "Forward": "none"
                            }
                        },
                        "TrustedSigners": {
                            "Enabled": False,
                            "Quantity": 0
                        },
                        "ViewerProtocolPolicy": "redirect-to-https",
                        "MinTTL": 0,
                        "MaxTTL": 2628000,
                        "DefaultTTL": 86400,
                        "AllowedMethods": {
                            "Quantity": 2,
                            "Items": ["GET", "HEAD"]
                        }
                    },
                    "Comment": "Distribution of %s.s3.amazonaws.com" % (
                        self.constants["BUCKET"]),
                    "Enabled": True
                }
            )
            print "Cloudfront distribution created"
        except botocore.exceptions.ClientError as e:
            print e
            sys.exit()

    def create_user_table(self):
        """ Creates a user table. """
        with open("dynamo/user_table.json", "r") as thefile:
            user_table_json = json.loads(thefile.read())
        user_table_json["TableName"] = self.constants["USER_TABLE"]

        try:
            print "Creating table: %s" % (self.constants["USER_TABLE"])
            dynamodb = boto3.client("dynamodb")
            user_table = dynamodb.create_table(**user_table_json)
            self.wait_for_table(user_table)
            print "User table created"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def create_token_table(self):
        """ Creates a token table. """
        with open("dynamo/token_table.json", "r") as thefile:
            token_table_json = json.loads(thefile.read())
        token_table_json["TableName"] = self.constants["TOKEN_TABLE"]

        try:
            print "Creating table: %s" % (self.constants["TOKEN_TABLE"])
            dynamodb = boto3.client("dynamodb")
            token_table = dynamodb.create_table(**token_table_json)
            self.wait_for_table(token_table)
            print "Token table created"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def create_item_table(self):
        """ Creates a blog table. """
        with open("dynamo/item_table.json", "r") as thefile:
            item_table_json = json.loads(thefile.read())
        item_table_json["TableName"] = self.constants["ITEM_TABLE"]

        try:
            print "Creating table: %s" % (self.constants["ITEM_TABLE"])
            dynamodb = boto3.client("dynamodb")
            item_table = dynamodb.create_table(**item_table_json)
            self.wait_for_table(item_table)
            print "Item table created"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def create_blog_table(self):
        """ Creates a blog table. """
        with open("dynamo/blog_table.json", "r") as thefile:
            blog_table_json = json.loads(thefile.read())
        blog_table_json["TableName"] = self.constants["BLOG_TABLE"]

        try:
            print "Creating table: %s" % (self.constants["BLOG_TABLE"])
            dynamodb = boto3.client("dynamodb")
            blog_table = dynamodb.create_table(**blog_table_json)
            self.wait_for_table(blog_table)
            print "Blog table created"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def create_page_table(self):
        """ Creates a page table. """
        with open("dynamo/page_table.json", "r") as thefile:
            page_table_json = json.loads(thefile.read())
        page_table_json["TableName"] = self.constants["PAGE_TABLE"]

        try:
            print "Creating table: %s" % (self.constants["PAGE_TABLE"])
            dynamodb = boto3.client("dynamodb")
            page_table = dynamodb.create_table(**page_table_json)
            self.wait_for_table(page_table)
            print "Page table created"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def create_role_table(self):
        """ Creates a role table. """
        with open("dynamo/role_table.json", "r") as thefile:
            role_table_json = json.loads(thefile.read())
        role_table_json["TableName"] = self.constants["ROLE_TABLE"]

        try:
            print "Creating table: %s" % (self.constants["ROLE_TABLE"])
            dynamodb = boto3.client("dynamodb")
            role_table = dynamodb.create_table(**role_table_json)
            self.wait_for_table(role_table)
            print "Role table created"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def create_table(self, schema_loc, table_id):
        """ Creates a table. """
        with open(schema_loc, "r") as thefile:
            table_json = json.loads(thefile.read())
        table_json["TableName"] = self.constants[table_id]
        try:
            print "Creating table: %s" % (self.constants[table_id])
            dynamodb = boto3.client("dynamodb")
            role_table = dynamodb.create_table(**table_json)
            self.wait_for_table(role_table)
            print "Created table: %s" % (self.constants[table_id])
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def wait_for_table(self, table):
        """ Waits for a table to finish being created. """
        # Wait for dynamo to acknowledge a table is being created
        table_creating = True
        retries = 10
        while table_creating and retries > 0:
            try:
                dynamodb = boto3.client("dynamodb")
                response = dynamodb.describe_table(
                    TableName=table["TableDescription"]["TableName"])
                table_creating = False
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "ResourceNotFoundException":
                    retries -= 1
                    time.sleep(0.5)
                else:
                    print e.response["Error"]["Code"]
                    print e.response["Error"]["Message"]
                    sys.exit()

        # Wait while the table creates
        while response["Table"]["TableStatus"] == "CREATING":
            time.sleep(0.1)
            response = dynamodb.describe_table(
                TableName=table["TableDescription"]["TableName"])

    def create_admin_user_db_entry(self):
        """ Creates an entry in the user database that represents an admin """
        with open("dynamo/user.json", "r") as thefile:
            admin_user_json = json.loads(thefile.read())
        admin_user_json["TableName"] = self.constants["USER_TABLE"]
        admin_user_json["Item"]["ID"] = {"S": str(uuid.uuid4())}

        try:
            print "Creating admin db entry"
            dynamodb = boto3.client("dynamodb")
            dynamodb.put_item(**admin_user_json)
            print "Admin db entry created"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def create_admin_role_db_entry(self):
        """ Creates an entry in the role database that represents an admin """
        with open("dynamo/role.json", "r") as thefile:
            admin_role_json = json.loads(thefile.read())
        admin_role_json["TableName"] = self.constants["ROLE_TABLE"]

        try:
            print "Creating admin role db entry"
            dynamodb = boto3.client("dynamodb")
            dynamodb.put_item(**admin_role_json)
            print "Admin role db entry created"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def create_db_entry(self, item_schema_loc, const_table_id):
        """ Creates an entry in dynamo with item location
         and  destination table id """
        with open(item_schema_loc, "r") as thefile:
            item_json = json.loads(thefile.read())
        item_json["TableName"] = self.constants[const_table_id]
        try:
            print "Creating " + const_table_id + " db entry"
            dynamodb = boto3.client("dynamodb")
            dynamodb.put_item(**item_json)
            print "Entity db " + const_table_id + " created"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def update_lambda(self, prefix=""):
        try:
            lmda = boto3.client("lambda")
            lmda.update_function_code(
                FunctionName=self.constants["LAMBDA_FUNCTION"+prefix],
                ZipFile=AwsFunc.zip_lambda(),
            )
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def create_lambda_function(self, prefix=""):
        """ Creates a lamda function and uploads AWS CMS to to it """

        lmda_role = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        })

        # Create the lambda iam role
        try:
            print "Creating iam role: %s" % (self.constants["LAMBDA_ROLE" + prefix])
            iam = boto3.client("iam")
            lambda_role_name = self.constants["LAMBDA_ROLE" + prefix]
            lambda_role = iam.create_role(
                RoleName=lambda_role_name,
                AssumeRolePolicyDocument=lmda_role
            )

            # Attach permissions to the lambda role
            iam.attach_role_policy(
                RoleName=lambda_role_name,
                PolicyArn="arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
            )
            iam.attach_role_policy(
                RoleName=lambda_role_name,
                PolicyArn=("arn:aws:iam::aws:"
                           "policy/service-role/AWSLambdaBasicExecutionRole")
            )
            iam.attach_role_policy(
                RoleName=lambda_role_name,
                PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess"
            )
            iam.attach_role_policy(
                RoleName=lambda_role_name,
                PolicyArn="arn:aws:iam::aws:policy/AmazonCognitoPowerUser"
            )
            print "Role created"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

        # Necessary as it can take a few seconds for an iam role to be usable
        print "Waiting for role to be usable"
        time.sleep(10)

        # Store constants file in lambda directory
        self.store_lambda_constants()

        # Create the lambda function
        try:
            print "Creating lambda function"
            lmda = boto3.client("lambda")
            lambda_function = lmda.create_function(
                FunctionName=self.constants["LAMBDA_FUNCTION" + prefix],
                Runtime="python2.7",
                Role=lambda_role["Role"]["Arn"],
                Handler="controller.handler" + prefix,
                Code={"ZipFile": AwsFunc.zip_lambda()},
                Description=("Aws cms central management function designed to "
                             "handle any API Gateway request"),
                MemorySize=512,
                Timeout=10
            )
            print "Function created"
            self.constants["LAMBDA_FUNCTION_ARN" + prefix] = (
                lambda_function["FunctionArn"])
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

        self.create_api_invocation_uri(prefix=prefix)
        self.remove_lambda_constants()

    def create_rest_api(self):
        """ Creates the api gateway and links it to the lambda function """
        try:
            api_gateway = boto3.client("apigateway")

            print "Creating the rest api"
            rest_api = api_gateway.create_rest_api(
                name=self.constants["REST_API"]
            )
            print "Rest api created"

            self.constants["REST_API_ID"] = rest_api["id"]
            rest_api_resource = api_gateway.get_resources(
                restApiId=self.constants["REST_API_ID"]
            )
            self.constants["REST_API_ROOT_ID"] = (
                rest_api_resource["items"][0]["id"])
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

        self.create_api_permissions_uri()
        self.create_api_url()

    def create_http_api_resource(self, api_gateway, rest_api_id, rest_api_other_id, path):
        resource_resp = api_gateway.create_resource(
            restApiId=rest_api_id,
            parentId=rest_api_other_id,  # resource id for the Base API path
            pathPart=path
        )
        return resource_resp

    def create_http_method(self, methodType , path):
        """
        Creates the api gateway and links it to the lambda function.

        :param methodType: http method such as GET,POST,DELETE,PUT,etc. all in caps
        :param path: path to call the lambda functions e.g. 'root' = "/" or 'other' = '/other'
        """
        try:
            api_gateway = boto3.client("apigateway")

            print "Creating the rest api"

            rest_api_id = self.constants["REST_API_ID"]
            if path != 'root':
                if not "REST_API_"+path+ "_ID" in self.constants:
                    resource_resp = self.create_http_api_resource(api_gateway, self.constants["REST_API_ID"], self.constants["REST_API_ROOT_ID"], path)

                    rest_api_other_id = resource_resp['id']
                    self.constants["REST_API_" + path + "_ID"] = resource_resp['id']
                else:
                    rest_api_other_id = self.constants["REST_API_"+path+"_ID"]
            else:
                rest_api_other_id = self.constants["REST_API_ROOT_ID"]

            if methodType == 'POST':
                apigatewaysetup.apiGatewaySetup.create_post_method(self,api_gateway, rest_api_id, rest_api_other_id)
            elif methodType == 'GET':
                apigatewaysetup.apiGatewaySetup.create_get_method(self,api_gateway, rest_api_id, rest_api_other_id)
            elif methodType == 'DELETE':
                apigatewaysetup.apiGatewaySetup.create_delete_method(self,api_gateway, rest_api_id, rest_api_other_id)
            elif methodType == 'PUT':
                apigatewaysetup.apiGatewaySetup.create_put_method(self, api_gateway, rest_api_id, rest_api_other_id)
            elif methodType == 'OPTION':
                apigatewaysetup.apiGatewaySetup.create_options_method(self,api_gateway, rest_api_id, rest_api_other_id)


        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

        self.create_api_permissions_uri()
        self.create_api_url()


    def deploy_api(self, prefix=""):

        try:
            api_gateway = boto3.client("apigateway")
            rest_api_id = self.constants["REST_API_ID"]

            print "Deploying api"
            # Create a deployment of the rest api
            api_gateway.create_deployment(
                restApiId=rest_api_id,
                stageName="prod"
            )

            lmda = boto3.client("lambda")
            function_name = self.constants["LAMBDA_FUNCTION" + prefix]
            api_permissions_uri = self.constants["API_PERMISSIONS_URI"]

            # Give the api deployment permission to trigger the lambda function
            lmda.add_permission(
                FunctionName=function_name,
                StatementId="7rbvfF87f67",
                Action="lambda:InvokeFunction",
                Principal="apigateway.amazonaws.com",
                SourceArn=api_permissions_uri
            )
            print "Api deployed"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

    def store_lambda_constants(self):
        """ Stores aws service constants in the lambda directory """
        with open("lambda/constants.json", "w") as constants_file:
            constants_file.write(json.dumps(self.constants, indent=4,
                                            sort_keys=True))

    def save_constants(self):
        """ Stores aws service constants in a file """
        constants_file_name = "%s-constants.json" % (self.cms_prefix)
        with open(constants_file_name, "w") as constants_file:
            constants_file.write(json.dumps(self.constants, indent=4,
                                            sort_keys=True))

        if not os.path.isfile("./installed.json"):
            with open("installed.json", "w") as installed:
                installed.write(json.dumps({"1": self.cms_prefix}, indent=4,
                                           sort_keys=True))
        else:
            with open("installed.json", "r") as installed:
                installed_json = json.loads(installed.read())
            next_key = len(installed_json.keys()) + 1
            installed_json[next_key] = self.cms_prefix
            with open("installed.json", "w") as installed:
                installed.write(json.dumps(installed_json, indent=4,
                                           sort_keys=True))

    def remove_lambda_constants(self):
        """ Removes aws service constants from the lambda directory """
        os.remove("lambda/constants.json")

    def create_api_invocation_uri(self, prefix):
        """ Creates an api invocation uri """
        self.constants["API_INVOCATION_URI"] = (
                                                   "arn:aws:apigateway:%s:lambda:"
                                                   "path/2015-03-31/functions/%s/invocations"
                                               ) % (self.region, self.constants["LAMBDA_FUNCTION_ARN"+prefix])

    def create_api_permissions_uri(self):
        """ Creates the uri that is needed for giving the api deployment
        permission to trigger the lambda function
        """
        # arn:aws:execute-api:us-east-1:*:*
        self.constants["API_PERMISSIONS_URI"] = (
                                                    "arn:aws:execute-api:%s:%s:%s/*/*/*"
                                                ) % (self.region, AwsFunc.get_account_id(),
                                                     self.constants["REST_API_ID"])

    def create_api_url(self):
        """ Creates the url needed to send requests to the api gateway """
        self.constants["API_URL"] = (
            "https://%s.execute-api.%s.amazonaws.com/prod" % (
                self.constants["REST_API_ID"], self.region))

    def print_login_link(self):
        print "Username: email@gmail.com"
        print "Password: password123"
        print "Login at: https://s3.amazonaws.com/%s/HTML/login.html" % (
            self.constants["BUCKET"])

    @staticmethod
    def get_account_id():
        sts = boto3.client("sts")
        return sts.get_caller_identity()["Account"]

    @staticmethod
    def zip_lambda():
        """ Zips all files needed to create the controller function and stores
        them in an object that will be uploaded to lambda.
        """
        # Don't zip these files
        ignore_files = ["controller.zip", "role_policy.json"]

        # Zip the files and store them in a buffer
        zip_data = BytesIO()
        zipf = zipfile.ZipFile(zip_data, "w")
        for root, dirs, files in os.walk("lambda"):
            for fl in files:
                if fl not in ignore_files:
                    path_to_file = os.path.join(root, fl)
                    file_key = path_to_file[7:]
                    zipf.write(path_to_file, arcname=file_key)
        zipf.close()

        # Write the buffer to a variable and return it
        zip_data.seek(0)
        data = zip_data.read()
        zip_data.close()
        return data

    @staticmethod
    def createDbInstance():
        rds = boto3.client('rds')
        try:
            response = rds.create_db_instance(
                DBName='MySQL',
                DBInstanceIdentifier='dbserver',
                MasterUsername='dbadmin',
                MasterUserPassword='abcdefg123456789',
                DBInstanceClass='db.t2.micro',
                Engine='mysql',
                AllocatedStorage=5)
        except Exception as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()
