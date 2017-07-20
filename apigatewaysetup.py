import botocore
import sys

"""
# apigatewaysetup.py
# Author: Wilson Joe
# Date: N/D
# Edited: 17/07/2017 | Wilson Joe
"""

class apiGatewaySetup:
    @staticmethod
    def create_post_method(self, api_gateway, rest_api_id, rest_api_root_id):
        """
                Creates the post method and links it to the lambda function.

                :param api_gateway: api gateway reference from boto3.client("apigateway")
                :param rest_api_id: id of API gateway
                :param rest_api_root_id: id of API parent path
        """

        print "Adding POST method to rest api"

        try:
            # Add a POST method to the rest api
            api_gateway.put_method(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="POST",
                authorizationType="NONE",
                requestParameters={
                    "method.request.header.Cookie": False
                }
            )

            # Put integration in the POST method
            api_gateway.put_integration(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="POST",
                type="AWS",
                passthroughBehavior="NEVER",
                integrationHttpMethod="POST",
                uri=self.constants["API_INVOCATION_URI"],
                requestTemplates={
                    "application/json": (
                        "#if($input.params(\"Cookie\") && $input.params(\"Cookie\") != \"\") "
                        "{"
                        "\"body\": $input.body, "
                        "\"token\": \"$input.params(\"Cookie\")\", "
                        "\"headers\": { #foreach($header in $input.params().header.keySet()) \"$header\": \"$util.escapeJavaScript($input.params().header.get($header))\" #if($foreach.hasNext),#end #end}, "
                        "\"method\": \"$context.httpMethod\","
                        "\"params\": { #foreach($param in $input.params().path.keySet()) \"$param\": \"$util.escapeJavaScript($input.params().path.get($param))\" #if($foreach.hasNext),#end #end }, "
                        "\"query\": { #foreach($queryParam in $input.params().querystring.keySet()) \"$queryParam\": \"$util.escapeJavaScript($input.params().querystring.get($queryParam))\" #if($foreach.hasNext),#end #end}"
                        "}"
                        "#else"
                        "{"
                        "\"body\": $input.body, "
                        "\"headers\": { #foreach($header in $input.params().header.keySet()) \"$header\": \"$util.escapeJavaScript($input.params().header.get($header))\" #if($foreach.hasNext),#end #end}, "
                        "\"method\": \"$context.httpMethod\","
                        "\"params\": { #foreach($param in $input.params().path.keySet()) \"$param\": \"$util.escapeJavaScript($input.params().path.get($param))\" #if($foreach.hasNext),#end #end }, "
                        "\"query\": { #foreach($queryParam in $input.params().querystring.keySet()) \"$queryParam\": \"$util.escapeJavaScript($input.params().querystring.get($queryParam))\"#if($foreach.hasNext),#end #end}"
                        "}"
                        "#end"
                    )
                }
            )

            # Put a 200 method response in the POST method
            api_gateway.put_method_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="POST",
                statusCode="200",
                responseParameters={
                    "method.response.header.Set-Cookie": False,
                    "method.response.header.Access-Control-Allow-Credentials": False,
                    "method.response.header.Access-Control-Allow-Origin": False
                },
                responseModels={
                    "application/json": "Empty"
                }
            )

            # Put a 200 integration response in the POST method
            api_gateway.put_integration_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="POST",
                statusCode="200",
                responseParameters={
                    "method.response.header.Set-Cookie": (
                        "integration.response.body.Set-Cookie"),
                    "method.response.header.Access-Control-Allow-Credentials": (
                        "\'true\'"),
                    "method.response.header.Access-Control-Allow-Origin": (
                        "\'https://s3.amazonaws.com\'")
                },
                responseTemplates={
                    "application/json": "$input.path('$.body')"
                }
            )

            # Put a 400 method response in the POST method
            api_gateway.put_method_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="POST",
                statusCode="400",
                responseParameters={
                    "method.response.header.Access-Control-Allow-Credentials": False,
                    "method.response.header.Access-Control-Allow-Origin": False
                },
                responseModels={
                    "application/json": "Empty"
                }
            )

            # Put a 400 integration response in the POST method
            api_gateway.put_integration_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="POST",
                statusCode="400",
                selectionPattern=".*'status': 400.*",
                responseParameters={
                    "method.response.header.Access-Control-Allow-Credentials": (
                        "\'true\'"),
                    "method.response.header.Access-Control-Allow-Origin": (
                        "\'https://s3.amazonaws.com\'")
                },
                responseTemplates={
                    "application/json": "$input.path('$.errorMessage')"
                }
            )
            print "POST method added"

        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

        self.create_api_permissions_uri()
        self.create_api_url()

    @staticmethod
    def create_get_method(self, api_gateway, rest_api_id, rest_api_root_id):
        """
               Creates the get method and links it to the lambda function.

               :param api_gateway: api gateway reference from boto3.client("apigateway")
               :param rest_api_id: id of API gateway
               :param rest_api_root_id: id of API parent path
        """
        print "Adding GET method to rest api"

        try:
            # Add a POST method to the rest api
            api_gateway.put_method(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="GET",
                authorizationType="NONE",
                requestParameters={
                    "method.request.header.Cookie": False
                }
            )

            # Put integration in the GET method
            api_gateway.put_integration(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="GET",
                type="AWS",
                passthroughBehavior="NEVER",
                integrationHttpMethod="POST",
                uri=self.constants["API_INVOCATION_URI"],
                requestTemplates={
                    "application/json": (
                        "#if($input.params(\"Cookie\") && $input.params(\"Cookie\") != \"\") "
                        "{"
                        "\"body\": $input.body, "
                        "\"token\": \"$input.params(\"Cookie\")\", "
                        "\"headers\": { #foreach($header in $input.params().header.keySet()) \"$header\": \"$util.escapeJavaScript($input.params().header.get($header))\" #if($foreach.hasNext),#end #end}, "
                        "\"method\": \"$context.httpMethod\",\"params\": { #foreach($param in $input.params().path.keySet()) \"$param\": \"$util.escapeJavaScript($input.params().path.get($param))\" #if($foreach.hasNext),#end #end }, "
                        "\"query\": { #foreach($queryParam in $input.params().querystring.keySet()) \"$queryParam\": \"$util.escapeJavaScript($input.params().querystring.get($queryParam))\" #if($foreach.hasNext),#end #end}"
                        "}"
                        "#else"
                        "{"
                        "\"body\": $input.body, "
                        "\"headers\": { #foreach($header in $input.params().header.keySet()) \"$header\": \"$util.escapeJavaScript($input.params().header.get($header))\" #if($foreach.hasNext),#end #end}, "
                        "\"method\": \"$context.httpMethod\",\"params\": { #foreach($param in $input.params().path.keySet()) \"$param\": \"$util.escapeJavaScript($input.params().path.get($param))\" #if($foreach.hasNext),#end #end }, "
                        "\"query\": { #foreach($queryParam in $input.params().querystring.keySet()) \"$queryParam\": \"$util.escapeJavaScript($input.params().querystring.get($queryParam))\"#if($foreach.hasNext),#end #end}"
                        "}"
                        "#end"
                    )
                }
            )

            # Put a 200 method response in the POST method
            api_gateway.put_method_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="GET",
                statusCode="200",
                responseParameters={
                    "method.response.header.Set-Cookie": False,
                    "method.response.header.Access-Control-Allow-Credentials": False,
                    "method.response.header.Access-Control-Allow-Origin": False
                },
                responseModels={
                    "application/json": "Empty"
                }
            )

            # Put a 200 integration response in the GET method
            api_gateway.put_integration_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="GET",
                statusCode="200",
                responseParameters={
                    "method.response.header.Set-Cookie": (
                        "integration.response.body.Set-Cookie"),
                    "method.response.header.Access-Control-Allow-Credentials": (
                        "\'true\'"),
                    "method.response.header.Access-Control-Allow-Origin": (
                        "\'https://s3.amazonaws.com\'")
                },
                responseTemplates={
                    "application/json": "$input.path('$.body')"
                }
            )

            # Put a 400 method response in the GET method
            api_gateway.put_method_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="GET",
                statusCode="400",
                responseParameters={
                    "method.response.header.Access-Control-Allow-Credentials": False,
                    "method.response.header.Access-Control-Allow-Origin": False
                },
                responseModels={
                    "application/json": "Empty"
                }
            )

            # Put a 400 integration response in the GET method
            api_gateway.put_integration_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="GET",
                statusCode="400",
                selectionPattern=".*'status': 400.*",
                responseParameters={
                    "method.response.header.Access-Control-Allow-Credentials": (
                        "\'true\'"),
                    "method.response.header.Access-Control-Allow-Origin": (
                        "\'https://s3.amazonaws.com\'")
                },
                responseTemplates={
                    "application/json": "$input.path('$.errorMessage')"
                }
            )
            print "GET method added"

        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

        self.create_api_permissions_uri()
        self.create_api_url()

    @staticmethod
    def create_delete_method(self, api_gateway, rest_api_id, rest_api_root_id):
        """
               Creates the delete method and links it to the lambda function.

               :param api_gateway: api gateway reference from boto3.client("apigateway")
               :param rest_api_id: id of API gateway
               :param rest_api_root_id: id of API parent path
        """
        print "Adding DELETE method to rest api"

        try:
            # Add a DELETE method to the rest api
            api_gateway.put_method(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="DELETE",
                authorizationType="NONE",
                requestParameters={
                    "method.request.header.Cookie": False
                }
            )

            # Put integration in the POST method
            api_gateway.put_integration(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="DELETE",
                type="AWS",
                passthroughBehavior="NEVER",
                integrationHttpMethod="POST",
                uri=self.constants["API_INVOCATION_URI"],
                requestTemplates={
                    "application/json": (
                        "#if($input.params(\"Cookie\") && $input.params(\"Cookie\") != \"\") "
                        "{"
                        "\"body\": $input.body, "
                        "\"token\": \"$input.params(\"Cookie\")\", "
                        "\"headers\": { #foreach($header in $input.params().header.keySet()) \"$header\": \"$util.escapeJavaScript($input.params().header.get($header))\" #if($foreach.hasNext),#end #end}, "
                        "\"method\": \"$context.httpMethod\",\"params\": { #foreach($param in $input.params().path.keySet()) \"$param\": \"$util.escapeJavaScript($input.params().path.get($param))\" #if($foreach.hasNext),#end #end }, "
                        "\"query\": { #foreach($queryParam in $input.params().querystring.keySet()) \"$queryParam\": \"$util.escapeJavaScript($input.params().querystring.get($queryParam))\" #if($foreach.hasNext),#end #end}"
                        "}"
                        "#else"
                        "{"
                        "\"body\": $input.body, "
                        "\"headers\": { #foreach($header in $input.params().header.keySet()) \"$header\": \"$util.escapeJavaScript($input.params().header.get($header))\" #if($foreach.hasNext),#end #end}, "
                        "\"method\": \"$context.httpMethod\",\"params\": { #foreach($param in $input.params().path.keySet()) \"$param\": \"$util.escapeJavaScript($input.params().path.get($param))\" #if($foreach.hasNext),#end #end }, "
                        "\"query\": { #foreach($queryParam in $input.params().querystring.keySet()) \"$queryParam\": \"$util.escapeJavaScript($input.params().querystring.get($queryParam))\"#if($foreach.hasNext),#end #end}"
                        "}"
                        "#end"
                    )
                }
            )

            # Put a 200 method response in the DELETE method
            api_gateway.put_method_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="DELETE",
                statusCode="200",
                responseParameters={
                    "method.response.header.Set-Cookie": False,
                    "method.response.header.Access-Control-Allow-Credentials": False,
                    "method.response.header.Access-Control-Allow-Origin": False
                },
                responseModels={
                    "application/json": "Empty"
                }
            )

            # Put a 200 integration response in the DELETE method
            api_gateway.put_integration_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="DELETE",
                statusCode="200",
                responseParameters={
                    "method.response.header.Set-Cookie": (
                        "integration.response.body.Set-Cookie"),
                    "method.response.header.Access-Control-Allow-Credentials": (
                        "\'true\'"),
                    "method.response.header.Access-Control-Allow-Origin": (
                        "\'https://s3.amazonaws.com\'")
                },
                responseTemplates={
                    "application/json": "$input.path('$.body')"
                }
            )

            # Put a 400 method response in the DELETE method
            api_gateway.put_method_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="DELETE",
                statusCode="400",
                responseParameters={
                    "method.response.header.Access-Control-Allow-Credentials": False,
                    "method.response.header.Access-Control-Allow-Origin": False
                },
                responseModels={
                    "application/json": "Empty"
                }
            )

            # Put a 400 integration response in the DELETE method
            api_gateway.put_integration_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="DELETE",
                statusCode="400",
                selectionPattern=".*\"status\": 400.*",
                responseParameters={
                    "method.response.header.Access-Control-Allow-Credentials": (
                        "\'true\'"),
                    "method.response.header.Access-Control-Allow-Origin": (
                        "\'https://s3.amazonaws.com\'")
                },
                responseTemplates={
                    "application/json": "$input.path('$.errorMessage')"
                }
            )
            print "DELETE method added"

        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

        self.create_api_permissions_uri()
        self.create_api_url()

    @staticmethod
    def create_put_method(self, api_gateway, rest_api_id, rest_api_root_id):
        """
               Creates the put method and links it to the lambda function.

               :param api_gateway: api gateway reference from boto3.client("apigateway")
               :param rest_api_id: id of API gateway
               :param rest_api_root_id: id of API parent path
        """
        print "Adding PUT method to rest api"

        try:
            # Add a PUT method to the rest api
            api_gateway.put_method(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="PUT",
                authorizationType="NONE",
                requestParameters={
                    "method.request.header.Cookie": False
                }
            )

            # Put integration in the PUT method
            api_gateway.put_integration(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="PUT",
                type="AWS",
                passthroughBehavior="NEVER",
                integrationHttpMethod="POST",
                uri=self.constants["API_INVOCATION_URI"],
                requestTemplates={
                    "application/json": (
                        "#if($input.params(\"Cookie\") && $input.params(\"Cookie\") != \"\") "
                        "{"
                        "\"body\": $input.body, "
                        "\"token\": \"$input.params(\"Cookie\")\", "
                        "\"headers\": { #foreach($header in $input.params().header.keySet()) \"$header\": \"$util.escapeJavaScript($input.params().header.get($header))\" #if($foreach.hasNext),#end #end}, "
                        "\"method\": \"$context.httpMethod\",\"params\": { #foreach($param in $input.params().path.keySet()) \"$param\": \"$util.escapeJavaScript($input.params().path.get($param))\" #if($foreach.hasNext),#end #end }, "
                        "\"query\": { #foreach($queryParam in $input.params().querystring.keySet()) \"$queryParam\": \"$util.escapeJavaScript($input.params().querystring.get($queryParam))\" #if($foreach.hasNext),#end #end}"
                        "}"
                        "#else"
                        "{"
                        "\"body\": $input.body, "
                        "\"headers\": { #foreach($header in $input.params().header.keySet()) \"$header\": \"$util.escapeJavaScript($input.params().header.get($header))\" #if($foreach.hasNext),#end #end}, "
                        "\"method\": \"$context.httpMethod\",\"params\": { #foreach($param in $input.params().path.keySet()) \"$param\": \"$util.escapeJavaScript($input.params().path.get($param))\" #if($foreach.hasNext),#end #end }, "
                        "\"query\": { #foreach($queryParam in $input.params().querystring.keySet()) \"$queryParam\": \"$util.escapeJavaScript($input.params().querystring.get($queryParam))\"#if($foreach.hasNext),#end #end}"
                        "}"
                        "#end"
                    )
                }
            )

            # Put a 200 method response in the PUT method
            api_gateway.put_method_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="PUT",
                statusCode="200",
                responseParameters={
                    "method.response.header.Set-Cookie": False,
                    "method.response.header.Access-Control-Allow-Credentials": False,
                    "method.response.header.Access-Control-Allow-Origin": False
                },
                responseModels={
                    "application/json": "Empty"
                }
            )

            # Put a 200 integration response in the PUT method
            api_gateway.put_integration_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="PUT",
                statusCode="200",
                responseParameters={
                    "method.response.header.Set-Cookie": (
                        "integration.response.body.Set-Cookie"),
                    "method.response.header.Access-Control-Allow-Credentials": (
                        "\'true\'"),
                    "method.response.header.Access-Control-Allow-Origin": (
                        "\'https://s3.amazonaws.com\'")
                },
                responseTemplates={
                    "application/json": "$input.path('$.body')"
                }
            )

            # Put a 400 method response in the PUT method
            api_gateway.put_method_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="PUT",
                statusCode="400",
                responseParameters={
                    "method.response.header.Access-Control-Allow-Credentials": False,
                    "method.response.header.Access-Control-Allow-Origin": False
                },
                responseModels={
                    "application/json": "Empty"
                }
            )

            # Put a 400 integration response in the PUT method
            api_gateway.put_integration_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="PUT",
                statusCode="400",
                selectionPattern=".*\"status\": 400.*",
                responseParameters={
                    "method.response.header.Access-Control-Allow-Credentials": (
                        "\'true\'"),
                    "method.response.header.Access-Control-Allow-Origin": (
                        "\'https://s3.amazonaws.com\'")
                },
                responseTemplates={
                    "application/json": "$input.path('$.errorMessage')"
                }
            )
            print "PUT method added"

        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()

        self.create_api_permissions_uri()
        self.create_api_url()

    @staticmethod
    def create_options_method(self, api_gateway, rest_api_id, rest_api_root_id):
        """
               Creates the option method and links it to the lambda function.

               :param api_gateway: api gateway reference from boto3.client("apigateway")
               :param rest_api_id: id of API gateway
               :param rest_api_root_id: id of API parent path
        """
        try:
            print "Adding OPTIONS method to rest api"
            # Add an options method to the rest api
            api_gateway.put_method(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="OPTIONS",
                authorizationType="NONE"
            )

            # Set the put integration of the OPTIONS method
            api_gateway.put_integration(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="OPTIONS",
                type="MOCK",
                requestTemplates={
                    "application/json": "{\"statusCode\": 200}"
                }
            )

            # Set the put method response of the OPTIONS method
            api_gateway.put_method_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="OPTIONS",
                statusCode="200",
                responseParameters={
                    "method.response.header.Access-Control-Allow-Headers": False,
                    "method.response.header.Access-Control-Allow-Origin": False,
                    "method.response.header.Access-Control-Allow-Credentials": False,
                    "method.response.header.Access-Control-Allow-Methods": False
                },
                responseModels={
                    "application/json": "Empty"
                }
            )

            # Set the put integration response of the OPTIONS method
            api_gateway.put_integration_response(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="OPTIONS",
                statusCode="200",
                responseParameters={
                    "method.response.header.Access-Control-Allow-Headers": (
                        "\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,"
                        "X-Amz-Security-Token,Cookie,Accept,"
                        "Access-Control-Allow-Origin\'"
                    ),
                    "method.response.header.Access-Control-Allow-Origin": (
                        "\'https://s3.amazonaws.com\'"),
                    "method.response.header.Access-Control-Allow-Credentials": (
                        "\'true\'"),
                    "method.response.header.Access-Control-Allow-Methods": (
                        "\'POST,OPTIONS\'")
                },
                responseTemplates={
                    "application/json": ""
                }
            )
            print "OPTIONS method addded"
        except botocore.exceptions.ClientError as e:
            print e.response["Error"]["Code"]
            print e.response["Error"]["Message"]
            sys.exit()
