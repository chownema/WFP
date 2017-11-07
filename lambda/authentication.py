import datetime
import json
import uuid
import sys
import logging
import pymysql
import boto3
import botocore
from objects import signUp
import sqlscripts

class Authentication(object):
    @staticmethod
    def signUp(userData, listing_table):
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
        
        jsonObject = json.loads(json.dumps(userData))
        sign_up_data = signUp.signUpData(**jsonObject)

        rds_host = "wilsontest-aws-dbserver.cssvrk1hkcjd.us-east-1.rds.amazonaws.com"
        name = "wilsontestadmin"
        password = "wilsontests3cr3t95"
        db_name = "wilsontestAwsDB"
        port = 3306

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        try:
            conn = pymysql.connect(rds_host, user=name,
                                   passwd=password, db=db_name, connect_timeout=5)



            logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

            with conn.cursor() as cur:
                # cur.execute(sqlscripts.createUserTable)
                # return (sqlscripts.insertUserToUserTable % (sign_up_data.username, sign_up_data.password, sign_up_data.firstName, sign_up_data.lastName ,sign_up_data.phoneNumber, sign_up_data.mobilePhoneNumber))
                cur.execute(sqlscripts.insertUserToUserTable % (sign_up_data.username, sign_up_data.password, sign_up_data.firstName, sign_up_data.lastName ,sign_up_data.phoneNumber, sign_up_data.mobilePhoneNumber))
                conn.commit()
                cur.execute("SELECT LAST_INSERT_ID()")
                results = cur.fetchone()

        except Exception as e:
            logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
            sys.exit()
        return "Last inserted user id" % (str(results[0]))




