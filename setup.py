#!/usr/bin/python2.7

"""
# setup.py
# Author: Christopher Treadgold
# Date: N/D
# Edited: 07/08/2016 | Christopher Treadgold
"""

import cms_functions
import sys
import os

#read setup command line
if len(sys.argv) not in range(1, 4): #allow range between 0 to 3 which 0 is for python and 1 is setup.py itself, the rests are cms name and regional
    command = ''
    for arg in sys.argv:
        command += arg + ' '
    print 'Invalid command: ' + command
    print 'Usage: %s <cms_prefix (optional)> <region (optional)>' % sys.argv[0]
    sys.exit()

# Instantiate an AwsFunc class
if len(sys.argv) == 3:
    cms = cms_functions.AwsFunc(sys.argv[1], region=sys.argv[2])
elif len(sys.argv) == 2:
    cms = cms_functions.AwsFunc(sys.argv[1])
else:
    cms = cms_functions.AwsFunc("wilsontest")

# Debug new table and record

# entity_files = ["entity_user", "entity_supplier", "entity_client"]
# cms.create_table("dynamo/entity_table.json", "ENTITY_TABLE")
# cms.create_db_entry("dynamo/" + entity_files[2] + ".json", "ENTITY_TABLE")


# Create tje rest api
cms.create_rest_api()

# Create the lambda function

prefix = "SignUp".upper()
cms.create_lambda_function(prefix=prefix)
cms.create_http_method("POST", prefix)
cms.create_http_method("PUT", prefix)
cms.deploy_api(prefix=prefix)

prefix= "login".upper()
cms.create_lambda_function(prefix=prefix)
cms.create_http_method("POST", prefix)
cms.create_http_method("DELETE", prefix)
cms.deploy_api(prefix=prefix)

prefix= "user".upper()
cms.create_lambda_function(prefix=prefix)
cms.create_http_method("GET", prefix)
cms.deploy_api(prefix=prefix)

prefix= "listing".upper()
cms.create_lambda_function(prefix=prefix)
cms.create_http_method("GET", prefix)
cms.create_http_method("POST", prefix)
cms.deploy_api(prefix=prefix)

cms.create_item_table()

# Create the s3 bucket
# cms.create_bucket()
# Create the cloudfront distribution
# cms.create_cloudfront_distribution() TODO: Reactivate

# Create the dynamodb blog table
# cms.create_blog_table()
#
# # Create the dynamodb page table
# cms.create_page_table()
#
# # Create the dynamodb token table
# cms.create_token_table()
#
# # Create the dunamodb role table
# cms.create_role_table()
# # Add an admin role to the role table
# cms.create_admin_role_db_entry()
#
# # Create the dynamodb user table
# cms.create_user_table()
# # Add an admin to the user table
# cms.create_admin_user_db_entry()
#
# # Print the default login credentials and the login link
# cms.print_login_link()

# Saves the cms installation information
cms.save_constants()
