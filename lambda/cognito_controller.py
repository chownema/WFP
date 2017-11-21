import boto3
import botocore
import json
import hmac
import hashlib
import base64
from objects import signUp
from objects import confirmSignUpData
from objects import signIn
from custom_exception.bad_request_exception import bad_request_exception
import datetime


class Cognito(object):
    region = 'us-east-1'
    user_pool_id = 'us-east-1_20z10a4Je'
    app_client_id = '6p7jft98ldlapc0cisr9ur02n9'
    identity_pool_id = 'us-east-1:4df9fe2c-3ea7-438a-a7dc-455f704845ca'

    @staticmethod
    def sign_up(parameters, user_table):
        # return json.dumps(parameters)

        j = json.loads(json.dumps(parameters))
        userData = signUp.signUpData(**j)

        try:
            idp_client = boto3.client('cognito-idp')

            # remove hard code please
            CLIENTID = '6p7jft98ldlapc0cisr9ur02n9'
            CLIENTSECRET = '10an02100u8e0gjvlpp5a3kgu1lannoo262h1g5eujqadposut7p'

            msg = userData.username + CLIENTID
            dig = hmac.new(str(CLIENTSECRET).encode('utf-8'),
                           msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
            d2 = base64.b64encode(dig).decode()
            dig = d2

            resp = idp_client.sign_up(
                ClientId=CLIENTID,
                SecretHash=str(dig),
                Username=userData.username,
                Password=userData.password
            )


        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'UsernameExistsException':
                message = "Username exists. Please choose other username."
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                message = "Email address is not in the correct format."
            elif e.response['Error']['Code'] == 'InvalidPasswordException':
                message = "Password must have numeric characters, symbol and, upper and lower case characters."
            else:
                message = "Unexpected error: %s" % e

            bodyContent = {"ErrorDescription": message}
            raise bad_request_exception(json.dumps(bodyContent))

        createdDate = datetime.datetime.utcnow()
        items = {
            "ID": {"S": resp["UserSub"]},
            "Username": {"S": userData.username},
            "firstName": {"S": userData.firstName},
            "lastName": {"S": userData.lastName},
            "phoneNumber": {"S": userData.phoneNumber},
            "mobilePhoneNumber": {"S": userData.mobilePhoneNumber},
            "CreatedDate": {"S": createdDate.strftime("%d-%b-%Y %H:%M UTC")},
            "UpdatedDate": {"S": createdDate.strftime("%d-%b-%Y %H:%M UTC")}
        }
        # Put the items in the items table
        try:
            dynamodb = boto3.client("dynamodb")
            dynamodb.put_item(
                TableName=user_table, Item=items, ReturnConsumedCapacity="TOTAL"
            )
        except botocore.exceptions.ClientError as e:
            action = "Putting items in the items table"
            return {"error": e.response["Error"]["Code"],
                    "data": {"exception": str(e), "action": action}}

        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

    @staticmethod
    def confirm_sign_up(parameters):

        j = json.loads(json.dumps(parameters))
        stuff = confirmSignUpData.confirmSignUpData(**j)

        # remove hard code please
        CLIENTID = '6p7jft98ldlapc0cisr9ur02n9'
        CLIENTSECRET = '10an02100u8e0gjvlpp5a3kgu1lannoo262h1g5eujqadposut7p'

        msg = stuff.username + CLIENTID
        dig = hmac.new(str(CLIENTSECRET).encode('utf-8'),
                       msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()
        dig = d2

        try:
            idp_client = boto3.client('cognito-idp')
            resp = idp_client.confirm_sign_up(ClientId=CLIENTID,
                                              SecretHash=str(dig),
                                              Username=stuff.username,
                                              ConfirmationCode=stuff.confirm_code)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ExpiredCodeException':
                message = "Code is not matching."
            elif e.response['Error']['Code'] == 'UserNotFoundException':
                message = "No such user found."
            elif e.response['Error']['Code'] == 'CodeMismatchException':
                message = "Code is expired."
            else:
                message = "Unexpected error: %s" % e

            bodyContent = {"ErrorDescription": message}
            raise bad_request_exception(json.dumps(bodyContent))

        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

    @staticmethod
    def sign_in_admin(parameters):

        j = json.loads(json.dumps(parameters))
        signInData = signIn.signInData(**j)

        try:
            # remove hard code please
            CLIENTID = '6p7jft98ldlapc0cisr9ur02n9'
            CLIENTSECRET = '10an02100u8e0gjvlpp5a3kgu1lannoo262h1g5eujqadposut7p'
            USER_POOL_ID = 'us-east-1_20z10a4Je'

            msg = signInData.username+ CLIENTID
            dig = hmac.new(str(CLIENTSECRET).encode('utf-8'),
                           msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
            d2 = base64.b64encode(dig).decode()
            dig = d2

            # Get ID Token
            idp_client = boto3.client('cognito-idp')
            resp = idp_client.admin_initiate_auth(UserPoolId=USER_POOL_ID,
                                                  ClientId=CLIENTID,
                                                  AuthFlow='ADMIN_NO_SRP_AUTH',
                                                  AuthParameters={'USERNAME': signInData.username,
                                                                  'PASSWORD': signInData.password, 'SECRET_HASH': str(dig)})

            # user_data = Cognito.get_user(resp["AuthenticationResult"]["AccessToken"])

            # for user_info in user_data["UserAttributes"]:
            #     if user_info["Name"] == "sub":
            #         userId = user_info["Value"]
            #
            #         createdDate = datetime.datetime.utcnow()
            #         uniqueId = str(uuid.uuid4())
            #         items = {
            #             "ID": {"S": uniqueId},
            #             "UserId": {"S": userId},
            #             "AccessToken": {"S": resp["AuthenticationResult"]["AccessToken"]},
            #             "TokenType": {"S": resp["AuthenticationResult"]["TokenType"]},
            #             "RefreshToken": {"S": resp["AuthenticationResult"]["RefreshToken"]},
            #             "IdToken": {"S": resp["AuthenticationResult"]["IdToken"]},
            #             "CreatedDate": {"S": createdDate.strftime("%d-%b-%Y %H:%M UTC")}
            #         }
            #         # Put the items in the items table
            #         try:
            #             dynamodb = boto3.client("dynamodb")
            #             dynamodb.put_item(
            #                 TableName=token_table, Item=items, ReturnConsumedCapacity="TOTAL"
            #             )
            #         except botocore.exceptions.ClientError as e:
            #             action = "Putting items in the items table"
            #             return {"error": e.response["Error"]["Code"],
            #                     "data": {"exception": str(e), "action": action}}

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'NotAuthorizedException':
                message = "Incorrect username or password."
            elif e.response['Error']['Code'] == 'UserNotFoundException':
                message = "No such user found."
            else:
                message = "Unexpected error: %s" % e

            bodyContent = {"ErrorDescription": message}
            raise bad_request_exception(json.dumps(bodyContent))

        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

    @staticmethod
    def log_out(parameters):
        ci_client = boto3.client('cognito-idp')
        try:
            resp = ci_client.global_sign_out(
                AccessToken=str(parameters["Authorization"])
            )
        except botocore.exceptions.ClientError as e:
            message = "Unexpected error: %s" % e
            bodyContent = {"ErrorDescription": message}
            raise bad_request_exception(json.dumps(bodyContent))

        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

    @staticmethod
    def get_user(accessToken):
        ci_client = boto3.client('cognito-idp')

        try:
            resp = ci_client.get_user(
                AccessToken= accessToken
            )
        except botocore.exceptions.ClientError as e:
            message = "Unexpected error: %s" % e
            bodyContent = {"ErrorDescription": message}
            raise bad_request_exception(json.dumps(bodyContent))

        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

    @staticmethod
    def authorize(accessToken):

        ci_client = boto3.client('cognito-idp')

        try:
            resp = ci_client.get_user(
                AccessToken=str(accessToken)
            )
        except botocore.exceptions.ClientError as e:
            return None

        userAttributes = resp["UserAttributes"]

        for attr in userAttributes:
            if str(attr["Name"]).lower() == 'sub':
                return str(attr["Value"])

        return None

    @staticmethod
    def intAuthorize(accessToken):

        ci_client = boto3.client('cognito-idp')

        try:
            resp = ci_client.get_user(
                AccessToken=str(accessToken)
            )
        except botocore.exceptions.ClientError as e:
            return None


        return None


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = obj.__str__()
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object
