import botocore
import sys

"""
# api_gateway_setup.py
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
                    "method.request.header.Cookie": False,
                    "method.request.header.Authorization": False
                }
            )

            # Put integration in the POST method
            api_gateway.put_integration(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="POST",
                type="AWS_PROXY",
                passthroughBehavior="NEVER",
                integrationHttpMethod="POST",
                uri=self.constants["API_INVOCATION_URI"]
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
                    "method.request.header.Cookie": False,
                    "method.request.header.Authorization": False
                }
            )

            # Put integration in the GET method
            api_gateway.put_integration(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="GET",
                type="AWS_PROXY",
                passthroughBehavior="NEVER",
                integrationHttpMethod="POST",
                uri=self.constants["API_INVOCATION_URI"]
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
                    "method.request.header.Cookie": False,
                    "method.request.header.Authorization": False
                }
            )

            # Put integration in the POST method
            api_gateway.put_integration(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="DELETE",
                type="AWS_PROXY",
                passthroughBehavior="NEVER",
                integrationHttpMethod="POST",
                uri=self.constants["API_INVOCATION_URI"]
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
                    "method.request.header.Cookie": False,
                    "method.request.header.Authorization": False
                }
            )

            # Put integration in the PUT method
            api_gateway.put_integration(
                restApiId=rest_api_id,
                resourceId=rest_api_root_id,
                httpMethod="PUT",
                type="AWS_PROXY",
                passthroughBehavior="NEVER",
                integrationHttpMethod="POST",
                uri=self.constants["API_INVOCATION_URI"]
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
