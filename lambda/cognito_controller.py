import boto3
import botocore
import json
import hmac
import hashlib
import base64
from objects import signUp
from objects import confirmSignUpData
from objects import signIn
import datetime

class Cognito(object):

    @staticmethod
    def sign_up(parameters):
        j = json.loads(parameters)
        stuff = signUp.signUpData(**j)

        # return {"statusCode": 200, "headers": None, "body": str(json.dumps(stuff.__dict__))}

        try:
            idp_client = boto3.client('cognito-idp')

            msg = stuff.username + CLIENTID
            dig = hmac.new(str(CLIENTSECRET).encode('utf-8'),
                           msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
            d2 = base64.b64encode(dig).decode()
            dig = d2

            resp = idp_client.sign_up(
                ClientId= CLIENTID,
                SecretHash= str(dig),
                Username=stuff.username,
                Password=stuff.password,
                UserAttributes=[{'Name': 'email', 'Value': stuff.email}]
            )

        except botocore.exceptions.ClientError as e:
            return {"statusCode": 401, "headers": None, "body": str(stuff) + " : " + str(e)}

        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls= DateTimeEncoder)}

    @staticmethod
    def confirm_sign_up(parameters):

        j = json.loads(parameters)
        stuff = confirmSignUpData.confirmSignUpData(**j)

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
            return {"statusCode": 401, "headers": None, "body": str(e)}

        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls= DateTimeEncoder)}

    @staticmethod
    def sign_in_admin(parameters):

        j = json.loads(parameters)
        stuff = signIn.signInData(**j)

        msg = stuff.username + CLIENTID
        dig = hmac.new(str(CLIENTSECRET).encode('utf-8'),
                       msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()
        dig = d2

        # Get ID Token
        idp_client = boto3.client('cognito-idp')
        resp = idp_client.admin_initiate_auth(UserPoolId=USER_POOL_ID,
                                              ClientId= CLIENTID,
                                              AuthFlow='ADMIN_NO_SRP_AUTH',
                                              AuthParameters={'USERNAME': stuff.username, 'PASSWORD': stuff.password, 'SECRET_HASH':str(dig)})

        provider = 'cognito-idp.%s.amazonaws.com/%s' % (REGION, USER_POOL_ID)
        token = resp['AuthenticationResult']['IdToken']

        # Get IdentityId
        ci_client = boto3.client('cognito-identity')
        resp = ci_client.get_id(AccountId=ACCOUNT_ID,
                                IdentityPoolId=IDENTITY_POOL_ID,
                                Logins={provider: token})

        # Get Credentials
        resp = ci_client.get_credentials_for_identity(IdentityId=resp['IdentityId'],
                                                      Logins={provider: token})

        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls= DateTimeEncoder)}

    @staticmethod
    def get_user(parameters):
        ci_client = boto3.client('cognito-idp')
        resp = ci_client.get_user(
            AccessToken= str(parameters["Authorization"])
        )
        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

    @staticmethod
    def sign_in_cog(parameters):

        j = json.loads(parameters)
        stuff = signIn.signInData(**j)

        msg = stuff.username + CLIENTID
        dig = hmac.new(str(CLIENTSECRET).encode('utf-8'),
                       msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()
        dig = d2

        # Get ID Token
        idp_client = boto3.client('cognito-idp')
        resp = idp_client.admin_initiate_auth(UserPoolId=USER_POOL_ID,
                                              ClientId= CLIENTID,
                                              AuthFlow='ADMIN_NO_SRP_AUTH',
                                              AuthParameters={'USERNAME': stuff.username, 'PASSWORD': stuff.password, 'SECRET_HASH':str(dig)})

        return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls= DateTimeEncoder)}

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object =json.JSONEncoder.default(self, obj)
        return encoded_object
