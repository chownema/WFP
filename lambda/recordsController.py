"""
# dynamocontroller.py
# Author: Miguel Saavedra
# Date: 10/12/2016
"""

import datetime
import json
import uuid

import boto3
import botocore
from objects import blog

from boto3.dynamodb.conditions import Key, Attr

class RecordController(object):
    """ Provides functions for handling dynamo related requests """

    @staticmethod
    def get_records(table):
        """
        Function which is used to fetch all records from a table

        Expected Query
        "Query" : No query expected

        Expected table
        "table_name" : "BLOG_TABLE",
        """
        action = "Getting items from the " + table + " table"
        try:
            dynamodb = boto3.client("dynamodb")
            items = dynamodb.scan(
                TableName=table, 
                ConsistentRead=True
            )
        except botocore.exceptions.ClientError as e:
            return {
                "status" : "failed",
                "error_message": e.response["Error"]["Code"],
                "data": {"exception": str(e), "action": action}
            }

        return {"status": 200, "body": items["Items"]}

    @staticmethod
    def get_records_query(table, parameters):
        """
        Function which is used to fetch all records from a table

        Expected Query
        "Query" : TBC

        Expected table
        "table_name" : "BLOG_TABLE",
        """
        action = "Getting items from the " + table + " table"
        try:
            dynamodb = boto3.resource("dynamodb")
            dbTable = dynamodb.Table(table)
            items = dbTable.query(
                KeyConditionExpression=Key(parameters["hash_key"]).eq(parameters["hash_val"]) & 
                    Key(parameters["range_key"]).between(parameters["range_fval"], parameters["range_tval"]),
                IndexName=parameters["index_name"],
                ConsistentRead=False,
            )
        except botocore.exceptions.ClientError as e:
            return { 
                "status" : "failed",
                "error_message": e.response["Error"]["Code"],
                "data": {"exception": str(e), "action": action}
            }

        return {"status": 200, "body": items}

    @staticmethod
    def get_record(table, parameters):
        """
        Function which is used to fetch a specific record using the primary 
        key identifier

        Expected Query
        "Query" : ?ID={ID}

        Expected table
        "table_name" : "BLOG_TABLE",
        """
        action = "Getting item from the " + table + " table"
        try:
            dynamodb = boto3.client("dynamodb")
            item = dynamodb.get_item(
                TableName=table, Key={ "ID" : {"S": parameters}}
            )
        except botocore.exceptions.ClientError as e:
            return { 
                "status" : "failed",
                "error_message": e.response["Error"]["Code"],
                "data": {"exception": str(e), "action": action}
            }
        if not "Item" in item:
            return {
                "status" : "failed",
                "error": "InvalidItemSelection",
                "data": {"ID": parameters["ID"],  "action": action}}
            
        return {"status" : 200, "body": item["Item"]}
    
    @staticmethod
    def put_record(tableName, parameters):
        """
        Function which is used to insert a record into the respective dynamo table

        Expected parameter input value
        {
            "ID" : "123"
        }

        Expected table
        "table_name" : "BLOG_TABLE",

        """
        try:
            dynamodb = boto3.resource("dynamodb")
            table = dynamodb.Table(tableName)
            print "print :"  + json.dumps(parameters)
            j = json.loads(json.dumps(parameters))
            blogObject = blog.blog(**j)

            table.put_item(Item= blogObject.__dict__)

        except botocore.exceptions.ClientError as e:
            action = "Putting item in the " + tableName + " table"
            return { 
                "status" : 400,
                "error_message": str(e.response["Error"]["Code"]),
                "data": {"exception": str(e), "action": action}
            }

        return {"status" : 200, "body": str(json.dumps(blogObject.__dict__))}

    @staticmethod
    def remove_record(table, parameters):
        """
        Function which is used to remove a record into the respective dynamo table
        using a key identifier

        Expected Query
        "Query" : ?ID={ID}

        Expected table
        "table_name" : "BLOG_TABLE",
        """
        try:
            dynamodb = boto3.client("dynamodb")
            delete_response = dynamodb.delete_item(
                TableName=table,
                Key={"ID" : {"S": parameters["ID"]}}
            )
        except botocore.exceptions.ClientError as e:
            action = "Removing item in the " + table + " table"
            return { 
                "status" : "failed",
                "error_message": e.response["Error"]["Code"],
                "data": {"exception": str(e), "action": action}
            }

        return {"status": 200, "body":"Successfully removed item"}
        