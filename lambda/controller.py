"""
# controller.py
# Author: Miguel Saavedra
# Date: 10/12/2016
"""

import json

from cognito_controller import CognitoController
from custom_exception.bad_request_exception import bad_request_exception

def handlerSIGNUP(event, context):
    print "debug" + str(event)
    httpMethod = event["method"]
    with open("constants.json", "r") as resources_file:
        resources = json.loads(resources_file.read())
    try:
        if httpMethod == 'POST':
            parameter = event["body"]
            return CognitoController.sign_up(parameter)
        elif httpMethod == 'PUT':
            parameter = event["body"]
            return CognitoController.confirm_sign_up(parameter)
    except bad_request_exception as e:
        badRequestTemplate = json.dumps({"statusCode": 400, "body" : json.loads(str(e.message))})
        raise Exception(str(badRequestTemplate))
    except Exception as e:
        unknownErrorTemplate = json.dumps({"statusCode": 500,"body": json.loads(str(e.message))})
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
            return CognitoController.sign_in(parameter)
    except bad_request_exception as e:
        badRequestTemplate = json.dumps({"statusCode": 400, "body": json.loads(str(e.message))})
        raise Exception(str(badRequestTemplate))
    except Exception as e:
        unknownErrorTemplate = json.dumps({"statusCode": 500, "body": json.loads(str(e.message))})
        raise Exception(str(unknownErrorTemplate))

    return json.dumps({"statusCode": 405, "body": json.dumps({"error":"Operation not supported"})})
