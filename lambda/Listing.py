import datetime
import json
import uuid

import boto3
import botocore
from cognito_controller import Cognito
from boto3.dynamodb.conditions import Key, Attr

class Listing(object):

    @staticmethod
    def get_all_listings(header,listing_table):

        userId = Cognito.authorize(header["Authorization"])

        if userId is None:
            return {"statusCode": 401}

        try:
            dynamodb = boto3.client("dynamodb")
            items = dynamodb.scan(
                TableName=listing_table, ConsistentRead=True
            )
        except botocore.exceptions.ClientError as e:
            action = "Fetching listing from the item table"
            return {"error": e.response["Error"]["Code"],
                    "data": {"exception": str(e), "action": action}}

        if not "Items" in items:
            action = "Fetching listing from the item table"
            return {"error": "noItems", "data": {"action": action}}

        data = []

        for item in items["Items"]:
            data.append( Listing.convert_item(item))

        resp = {"data": data}

        return {"statusCode": 200, "headers": None, "body": json.dumps(resp)}

    @staticmethod
    def put_item(header, body, listing_table):
        """ Puts a items in the items table """
        userId = Cognito.authorize(header["Authorization"])

        if userId is None:
            return {"statusCode": 401}

        # Create the items entry
        saved_date = datetime.datetime.utcnow()
        saved_date = saved_date.strftime("%d-%b-%Y %H:%M UTC")
        uniqueId = str(uuid.uuid4())
        items = {
            "ID": {"S": uniqueId},
            "UserID": {"S": userId},
            "SavedDate": {"S": saved_date},
            "Title": {"S": body["title"]}
        }
        # Put the items in the items table
        try:
            dynamodb = boto3.client("dynamodb")
            put_response = dynamodb.put_item(
                TableName=listing_table, Item=items, ReturnConsumedCapacity="TOTAL"
            )
        except botocore.exceptions.ClientError as e:
            action = "Putting items in the items table"
            return {"error": e.response["Error"]["Code"],
                    "data": {"exception": str(e), "action": action}}

        resp = {"data": Listing.convert_item(items)}

        return {"statusCode": 200, "headers": None, "body": json.dumps(resp)}

    @staticmethod
    def convert_item(items):

        resp = {}

        for item in items.keys():
            resp[item]=  items[item]["S"]

        return resp