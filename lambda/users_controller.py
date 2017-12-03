import datetime
import json
from objects import signUp
from sql_utils import sql_functions
from sql_utils import sql_scripts

class User(object):
    @staticmethod
    def add_user(userId, username, userData, resources):
        try:
            json_object = json.loads(userData)
            sign_up_data = signUp.signUpData(**json_object)

            sql_script = sql_scripts.User["Create"].format(userId, username, sign_up_data.firstName, sign_up_data.lastName, sign_up_data.phoneNumber, sign_up_data.mobilePhoneNumber)
            user_id = sql_functions.sql_functions.insert_into_table(resources, sql_script)

            created_user_data = User.get_user(user_id, resources)

            resp = created_user_data["body"]

            return {"statusCode": 201, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

        except Exception as e:
            return {"statusCode": 500, "headers": None, "body": str(e)}

    @staticmethod
    def list_users(resources):
        try:
            sql_script = sql_scripts.User["List"]
            users_data = sql_functions.sql_functions.list_data_from_table(resources, sql_script)
            resp ={
                "users": users_data
            }

            return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}
        except Exception as e:
            return {"statusCode": 500, "headers": None, "body": str(e)}

    @staticmethod
    def get_user(userId, resources):
        try:
            sql_script = sql_scripts.User["Get"].format(userId)
            resp = sql_functions.sql_functions.list_data_from_table(resources, sql_script)
            if len(resp) == 0:
                resp = {
                    "message":"not found."
                }
                return {"statusCode": 404, "headers": None, "body": json.dumps(resp)}
            else:
                return {"statusCode": 200, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

        except Exception as e:
            return {"statusCode": 500, "headers": None, "body": str(e)}

    @staticmethod
    def update_user(userId, userData, resources):
        try:
            json_object = json.loads(userData)
            sign_up_data = signUp.signUpData(**json_object)

            sql_script = sql_scripts.User["Update"].format(sign_up_data.firstName,
                                                           sign_up_data.lastName, sign_up_data.phoneNumber,
                                                           sign_up_data.mobilePhoneNumber, userId)
            sql_functions.sql_functions.execute_sql_command(resources, sql_script)

            resp = {
                "message": "user information updated successfully."
            }

            return {"statusCode": 201, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

        except Exception as e:
            return {"statusCode": 500, "headers": None, "body": str(e)}

    @staticmethod
    def delete_user(userId, resources):
        try:
            sql_script = sql_scripts.User["Delete"].format(userId)
            sql_functions.sql_functions.insert_into_table(resources, sql_script)

            resp = {
                "message":"user deleted successfully."
            }

            return {"statusCode": 204, "headers": None, "body": json.dumps(resp)}

        except Exception as e:
            return {"statusCode": 500, "headers": None, "body": str(e)}

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = obj.__str__()
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object