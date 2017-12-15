import datetime
import json
from objects import signUp
from sql_utils import sql_functions
from sql_utils import sql_scripts

class me_functions(object):

    """
        function: Add myself (USER) into the database
        
        Params:
        @userId = cognito userId
        @username = cognito username
        @userData = JSON data which contains user data
        @resources = contains data to be used to access DB
        
        return: 
        - 201 created if success
        - 409 conflict
        - 500 internal server error
    """
    @staticmethod
    def add_me(userId, username, userData, resources):
        try:
            json_object = json.loads(userData)
            sign_up_data = signUp.signUpData(**json_object)

            sql_script = sql_scripts.User["Create"].format(userId, username, sign_up_data.firstName, sign_up_data.lastName, sign_up_data.phoneNumber, sign_up_data.mobilePhoneNumber)
            user_id = sql_functions.sql_functions.insert_into_table(resources, sql_script)

            created_user_data = signUp.get_user(user_id, resources)

            resp = created_user_data["body"]

            return {"statusCode": 201, "headers": None, "body": json.dumps(resp, cls=DateTimeEncoder)}

        except Exception as e:
            return {"statusCode": 500, "headers": None, "body": str(e)}


    """
        function: Get myself (USER) into the database
        
        Params:
        @userId = cognito userId
        @username = cognito username
        @userData = JSON data which contains user data
        @resources = contains data to be used to access DB
        
        return: 
        - 201 created if success
        - 409 conflict
        - 500 internal server error
    """
    @staticmethod
    def get_me(userId, resources):
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
    def update_me(userId, userData, resources):
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
    def delete_me(userId, resources):
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