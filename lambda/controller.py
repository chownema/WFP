"""
# controller.py
# Author: Miguel Saavedra
# Date: 10/12/2016
"""

import json

from security import Security
from cognito_controller import Cognito
from authentication import Authentication
from Listing import Listing
from custom_exception.not_supported_exception import not_supported_exception
from custom_exception.bad_request_exception import bad_request_exception

import requests

def handlerSIGNUP(event, context):
    httpMethod = event["method"]
    with open("constants.json", "r") as resources_file:
        resources = json.loads(resources_file.read())
    try:
        if httpMethod == 'POST':
            parameter = event["body"]
            return Cognito.sign_up(parameter)
        elif httpMethod == 'PUT':
            parameter = event["body"]
            return Authentication.signUp(parameter, resources["ITEM_TABLE"])
            # return Cognito.confirm_sign_up(parameter)
    except bad_request_exception as e:
        badRequestTemplate = json.dumps({"statusCode": 400, "body" : json.loads(str(e.message))})
        raise Exception(str(badRequestTemplate))
    except Exception as e:
        unknownErrorTemplate = json.dumps({"statusCode": 500,"body": str(e.message)})
        raise Exception(str(unknownErrorTemplate))

    return json.dumps({"statusCode": 405, "body": json.dumps({"error":"Operation not supported"})})

def handlerLOGIN(event, context):
    print "debug" + str(event)
    httpMethod = event["method"]
    with open("constants.json", "r") as resources_file:
        resources = json.loads(resources_file.read())
    try:
        if httpMethod == 'POST':
            parameter = event["body"]
            return Cognito.sign_in_admin(parameter)
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
    print "debug" + str(event)
    httpMethod = event["method"]
    with open("constants.json", "r") as resources_file:
        resources = json.loads(resources_file.read())
    try:
        if httpMethod == 'GET':
            parameter = event["headers"]
            return Cognito.get_user(parameter)
    except bad_request_exception as e:
        badRequestTemplate = json.dumps({"statusCode": 400, "body": json.loads(str(e.message))})
        raise Exception(str(badRequestTemplate))
    except Exception as e:
        unknownErrorTemplate = json.dumps({"statusCode": 500, "body": json.loads(str(e.message))})
        raise Exception(str(unknownErrorTemplate))

    return json.dumps({"statusCode": 405, "body": json.dumps({"error":"Operation not supported"})})

def handlerLISTING(event, context):
    print "debug" + str(event)
    httpMethod = event["method"]
    with open("constants.json", "r") as resources_file:
        resources = json.loads(resources_file.read())
    try:
        if httpMethod == 'GET':
            parameter = event["headers"]
            return Listing.get_all_listings(parameter, resources["ITEM_TABLE"])
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