import boto3
import botocore
import json
from objects import signUp
from objects import confirmSignUpData
from objects import signIn
from custom_exception.bad_request_exception import bad_request_exception
from warrant import Cognito
import datetime


class CognitoController(object):
    region = 'us-east-1'
    user_pool_id = 'us-east-1_20z10a4Je'
    app_client_id = '6p7jft98ldlapc0cisr9ur02n9'
    identity_pool_id = 'us-east-1:4df9fe2c-3ea7-438a-a7dc-455f704845ca'
    account_id = 'xxxxxxxxxxxx'

    @staticmethod
    def sign_up(parameters):
        # return json.dumps(parameters)

        j = json.loads(json.dumps(parameters))
        stuff = signUp.signUpData(**j)

        try:
            u = Cognito('us-east-1_20z10a4Je', '6p7jft98ldlapc0cisr9ur02n9')
            resp = u.register(stuff.username, stuff.password, email=stuff.email)
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

        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

    @staticmethod
    def confirm_sign_up(parameters):

        j = json.loads(json.dumps(parameters))
        stuff = confirmSignUpData.confirmSignUpData(**j)

        try:
            u = Cognito('us-east-1_20z10a4Je', '6p7jft98ldlapc0cisr9ur02n9')

            resp = u.confirm_sign_up(stuff.confirm_code, username=stuff.username)

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
    def sign_in(parameters):

        j = json.loads(json.dumps(parameters))
        stuff = signIn.signInData(**j)

        try:
            u = Cognito('us-east-1_20z10a4Je', '6p7jft98ldlapc0cisr9ur02n9',
                        username=stuff.username)

            resp = u.authenticate(password=stuff.password)

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
    def get_user(parameters):
        ci_client = boto3.client('cognito-idp')
        resp = ci_client.get_user(
            AccessToken=str(parameters["Authorization"])
        )
        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

    @staticmethod
    def get_user(parameters):
        ci_client = boto3.client('cognito-idp')
        resp = ci_client.get_user(
            AccessToken=str(parameters["Authorization"])
        )
        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = obj.__str__()
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object
