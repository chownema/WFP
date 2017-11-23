import json
import sys
import logging
import pymysql
import sqlscripts
from sql_functions import sql_functions
from objects import signUp
import datetime

class User(object):
    @staticmethod
    def get_user(userId, resource):
        rds_host = "wilsontest-aws-dbserver.cssvrk1hkcjd.us-east-1.rds.amazonaws.com"
        username = resource["DB_INSTANCE_USERNAME"]
        password = resource["DB_INSTANCE_PASSWORD"]
        db_name = resource["DB_INSTANCE_NAME"]
        port = 3306

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        try:
            conn = pymysql.connect(rds_host, user=username,
                                   passwd=password, db=db_name, connect_timeout=5)

            logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


            if not sql_functions.sql_functions.checkTableExists(conn, "USERS"):
                conn.cursor().execute(sqlscripts.createUserTable)
                conn.commit()

            with conn.cursor() as cur:
                cur.execute(sqlscripts.getUserFromUserTable % (userId))
                resp = cur.fetchall()
                if len(resp) == 0:
                    resp = {
                        "message":"not found"
                    }
                    return {"statusCode": 404, "headers": None, "body": json.dumps(resp)}
                else:
                    return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

        except Exception as e:
            return {"statusCode": 500, "headers": None, "body": str(e)}

    @staticmethod
    def add_user(userId, username, userData, resource):
        rds_host = "wilsontest-aws-dbserver.cssvrk1hkcjd.us-east-1.rds.amazonaws.com"
        dbUsername = resource["DB_INSTANCE_USERNAME"]
        dbPassword = resource["DB_INSTANCE_PASSWORD"]
        db_name = resource["DB_INSTANCE_NAME"]
        port = 3306

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        try:
            conn = pymysql.connect(rds_host, user=dbUsername,
                                   passwd=dbPassword, db=db_name, connect_timeout=5)

            logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

            if not sql_functions.sql_functions.checkTableExists(conn, "USERS"):
                conn.cursor().execute(sqlscripts.createUserTable)
                conn.commit()

            with conn.cursor() as cur:
                cur.execute(sqlscripts.getUserFromUserTable % (userId))
                resp = cur.fetchall()
                if len(resp) > 0:
                    resp = {
                        "message": "cannot add user information"
                    }
                    return {"statusCode": 400, "headers": None, "body": json.dumps(resp)}
                else:
                    jsonObject = json.loads(userData)
                    sign_up_data = signUp.signUpData(**jsonObject)
                    args = (userId, username, sign_up_data.password, sign_up_data.firstName, sign_up_data.lastName, sign_up_data.phoneNumber, sign_up_data.mobilePhoneNumber)
                    cur.execute(sqlscripts.insertUserToUserTable, args)
                    conn.commit()
                    return {"statusCode": 200, "headers": None, "body": json.dumps(resp)}

        except Exception as e:
            return {"statusCode": 500, "headers": None, "body": str(e)}

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = obj.__str__()
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object