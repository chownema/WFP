"""
# sitesettings.py
# Author: Adam Campbell
# Date: 17/07/2016
"""

import datetime
import json
import uuid

import boto3
import botocore

class Site_Settings(object):
    """ Provides functions for handling SiteSettings related requests """
    
    @staticmethod
    def get_site_settings(bucket):
        return json.loads(Site_Settings.read_site_settings(bucket));

    @staticmethod
    def put_site_settings(site_name, site_description, facebook, twitter,
                          instagram, google_plus, footer, disqus_id, google_id,
                          primary_color, highlight_color, bucket):
        site_settings = json.loads(Site_Settings.read_site_settings(bucket))
        site_settings["site_name"] = site_name
        site_settings["site_description"] = site_description
        site_settings["facebook"] = facebook
        site_settings["twitter"] = twitter
        site_settings["instagram"] = instagram
        site_settings["google_plus"] = google_plus
        site_settings["footer"] = footer
        site_settings["disqus_id"] = disqus_id
        site_settings["google_id"] = google_id
        site_settings["primary_colour"] = primary_color
        site_settings["highlight_colour"] = highlight_color
        
        return Site_Settings.save_site_settings(site_settings, bucket)

    @staticmethod
    def get_nav_items(bucket):
        """ Reads the visitor navigation items from site settings JSON """
        # Get site setting JSON
        site_settings = json.loads(Site_Settings.read_site_settings(bucket))
        # Get nav item JSON
        nav_items = site_settings["nav"]
        # Return nav item data
        return {"data": nav_items}

    @staticmethod
    def put_nav_items(nav_items, bucket):
        """ Puts updated visitor navigation items into site settings """
        # Get site setting JSON
        site_settings = json.loads(Site_Settings.read_site_settings(bucket))
        # Set nav items
        site_settings["nav"] = nav_items
        # Save site setting JSON
        Site_Settings.save_site_settings(site_settings, bucket)
        return {"message": "Successfully saved nav items"}

    @staticmethod
    def read_site_settings(bucket):
        """ Reads the site settings JSON from an S3 Bucket """
        s3 = boto3.client('s3')
        fileName= "Content/site_settings.json"
        get_kwargs = {
            'Bucket': bucket,
            'Key': fileName
        }
        result =  s3.get_object(**get_kwargs)
        object_body = result['Body'].read()
        
        # Return Body of the Site Setting file
        return object_body

    @staticmethod
    def save_site_settings(site_settings, bucket):
        """ Saves site settings to an S3 Bucket """
        # Save site settings to s3
        try:
            s3 = boto3.client("s3")
            s3.put_object(
                Bucket=bucket, ACL="public-read", Body=json.dumps(site_settings),
                Key=("Content/site_settings.json"),
                ContentType="application/json"
            )
        except botocore.exceptions.ClientError as e:
            action = "Putting site settings in the bucket"
            return {"error": e.response["Error"]["Code"],
                    "data": {"exception": str(e), "action": action}}
        
        return {"message": "Successfully saved site settings"}