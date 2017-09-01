import boto3
import botocore
import json
import hmac
import hashlib
import base64
from objects import signUp
from objects import confirmSignUpData
from objects import signIn

class Cognito(object):
    region = 'us-east-1'
    user_pool_id = 'us-east-1_20z10a4Je'
    app_client_id = '6p7jft98ldlapc0cisr9ur02n9'
    identity_pool_id = 'us-east-1:4df9fe2c-3ea7-438a-a7dc-455f704845ca'
    account_id = 'xxxxxxxxxxxx'

    @staticmethod
    def sign_up(parameters):
        j = json.loads(parameters)
        stuff = signUp.signUpData(**j)

        # return {"statusCode": 200, "headers": None, "body": str(json.dumps(stuff.__dict__))}

        try:
            idp_client = boto3.client('cognito-idp')

            #remove hard code please
            CLIENTID = '6p7jft98ldlapc0cisr9ur02n9'
            CLIENTSECRET = '10an02100u8e0gjvlpp5a3kgu1lannoo262h1g5eujqadposut7p'

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

        return {"statusCode": 200, "headers": None, "body": json.dumps(json.loads(resp))}

    @staticmethod
    def confirm_sign_up(parameters):

        j = json.loads(parameters)
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
            return {"statusCode": 401, "headers": None, "body": str(e)}

        return {"statusCode": 200, "headers": None, "body": json.dumps(json.loads(resp))}

    @staticmethod
    def sign_in_admin(parameters):

        j = json.loads(parameters)
        stuff = signIn.signInData(**j)

        # remove hard code please
        CLIENTID = '6p7jft98ldlapc0cisr9ur02n9'
        CLIENTSECRET = '10an02100u8e0gjvlpp5a3kgu1lannoo262h1g5eujqadposut7p'

        REGION = 'us-east-1'
        USER_POOL_ID = 'us-east-1_20z10a4Je'

        IDENTITY_POOL_ID = 'us-east-1:4df9fe2c-3ea7-438a-a7dc-455f704845ca'
        ACCOUNT_ID = '265116334736'

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

        # provider = 'cognito-idp.%s.amazonaws.com/%s' % (REGION, USER_POOL_ID)
        # token = resp['AuthenticationResult']['IdToken']

        # # Get IdentityId
        # ci_client = boto3.client('cognito-identity')
        # resp = ci_client.get_id(AccountId=ACCOUNT_ID,
        #                         IdentityPoolId=IDENTITY_POOL_ID,
        #                         Logins={provider: token})
        #
        # # Get Credentials
        # resp = ci_client.get_credentials_for_identity(IdentityId=resp['IdentityId'],
        #                                               Logins={provider: token})
        return {"statusCode": 200, "headers": None, "body": json.dumps(json.loads(resp)) }
