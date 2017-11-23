"""
# controller.py
# Author: Miguel Saavedra
# Date: 10/12/2016
"""

import json

from Listing import Listing
from user import User
from cognito_controller import Cognito
from custom_exception.bad_request_exception import bad_request_exception


def handlerSIGNUP(event, context):
    httpMethod = event["httpMethod"]
    with open("constants.json", "r") as resources_file:
        resources = json.loads(resources_file.read())
    try:
        if httpMethod == 'POST':
            parameter = event["body"]
            return Cognito.sign_up(parameter)
        elif httpMethod == 'PUT':
            parameter = event["body"]
            return Cognito.confirm_sign_up(parameter)
    except bad_request_exception as e:
        badRequestTemplate = json.dumps({"statusCode": 400, "body" : json.loads(str(e.message))})
        raise Exception(str(badRequestTemplate))
    except Exception as e:
        unknownErrorTemplate = json.dumps({"statusCode": 500,"body": str(e.message)})
        raise Exception(str(unknownErrorTemplate))

    return json.dumps({"statusCode": 405, "body": json.dumps({"error":"Operation not supported"})})

def handlerLOGIN(event, context):
    httpMethod = event["httpMethod"]
    with open("constants.json", "r") as resources_file:
        resources = json.loads(resources_file.read())
    try:
        if httpMethod == 'POST':
            parameter = event["body"]
            return Cognito.sign_in(parameter)
        elif httpMethod == 'DELETE':
            parameter = event["headers"]
            return Cognito.log_out(parameter)
    except bad_request_exception as e:
        badRequestTemplate = json.dumps({"statusCode": 400, "body": json.loads(str(e.message))})
        raise Exception(str(badRequestTemplate))
    except Exception as e:
        unknownErrorTemplate = json.dumps({"statusCode": 500, "body": json.loads(str(e.message))})
        raise Exception(str(unknownErrorTemplate))

    return json.dumps({"statusCode": 405, "body": json.dumps({"error":"Operation not supported"})})

def handlerUSER(event, context):
    httpMethod = event["httpMethod"]
    with open("constants.json", "r") as resources_file:
        resources = json.loads(resources_file.read())
    try:
        if httpMethod == 'POST':
            parameter = event["body"]
            # userId = event["requestContext"]["authorizer"]["claims"]["sub"]
            userId = "695f5f6b-a7c9-4e98-8cc7-a98f977ca94b"
            return User.add_user(userId, parameter, resources)
        if httpMethod == 'GET':
            # userId = event["requestContext"]["authorizer"]["claims"]["sub"]
            userId = "695f5f6b-a7c9-4e98-8cc7-a98f977ca94b"
            username = "username2"
            return User.get_user(userId, username, resources)
    except bad_request_exception as e:
        badRequestTemplate = json.dumps({"statusCode": 400, "body": json.loads(str(e.message))})
        raise Exception(str(badRequestTemplate))
    except Exception as e:
        unknownErrorTemplate = json.dumps({"statusCode": 500, "body": json.loads(str(e.message))})
        raise Exception(str(unknownErrorTemplate))

    return json.dumps({"statusCode": 405, "body": json.dumps({"error":"Operation not supported"})})

def handlerLISTING(event, context):
    httpMethod = event["httpMethod"]

    with open("constants.json", "r") as resources_file:
        resources = json.loads(resources_file.read())
    try:
        if httpMethod == 'GET':
            parameter = event["headers"]
            return Listing.get_all_listings(event, parameter, resources["ITEM_TABLE"])
        if httpMethod == 'POST':
            header = event["headers"]
            body = event["body"]
            return Listing.put_item(header, body, resources["ITEM_TABLE"])
    except bad_request_exception as e:
        badRequestTemplate = json.dumps({"statusCode": 400, "body": json.loads(str(e.message))})
        raise Exception(str(badRequestTemplate))
    except Exception as e:
        unknownErrorTemplate = json.dumps({"statusCode": 500, "body": str(e.message)})
        raise Exception(str(unknownErrorTemplate))

    return json.dumps({"statusCode": 405, "body": json.dumps({"error":"Operation not supported"})})