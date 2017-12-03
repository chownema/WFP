import sql_scripts
import pymysql

class sql_functions(object):

    @staticmethod
    def get_db_connection(resources):
        try:
            rds_host = ""
            username = resources["DB_INSTANCE_USERNAME"]
            password = resources["DB_INSTANCE_PASSWORD"]
            db_name = resources["DB_INSTANCE_NAME"]
            conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)
            return conn
        except Exception as e:
            raise Exception(str(resources["DB_INSTANCE_USERNAME"]))

    @staticmethod
    def check_table_exists(resources, table_name):
        sql_script = sql_scripts.CommonScripts["CHECK_TABLE_EXISTS"].format(table_name)
        data = sql_functions.list_data_from_table(resources, sql_script)
        if len(data) == 1 and data[0] == 1:
            return True
        else:
            return False

    @staticmethod
    def create_all_table_if_not_exists(resources):
        try:
            for script in sql_scripts.SetUpScripts:
                sql_functions.execute_sql_command(resources, script)
        except Exception as e:
            raise Exception("Cannot Setup DB")

    @staticmethod
    def execute_sql_command(resources, sql_scripts):
        try:
            conn = sql_functions.get_db_connection(resources)
            with conn.cursor() as cursor:
                cursor.execute(sql_scripts)
                conn.commit()
        except Exception as e:
            raise Exception("Could create table in DB. Error: " + str(e))

    @staticmethod
    def insert_into_table(resources, sql_scripts):
        try:
            conn = sql_functions.get_db_connection(resources)
            with conn.cursor() as cursor:
                cursor.execute(sql_scripts)
                inserted_id =  conn.insert_id()
                conn.commit()
                return inserted_id
        except Exception as e:
            raise Exception("Could create table in DB. Error: " + str(e))

    @staticmethod
    def list_data_from_table(resources, sql_scripts):
        try:
            conn = sql_functions.get_db_connection(resources)
            with conn.cursor() as cursor:
                cursor.execute(sql_scripts)
                resp = cursor.fetchall()
                return resp
        except Exception as e:
            raise Exception("Could retrieve data from DB. Error:  " +  str(e))