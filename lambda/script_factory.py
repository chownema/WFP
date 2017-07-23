"""
# script_factory.oy
# Author: Miguel Saavedra
# Date: 23/07/2016
"""

import os
import json

class ScriptFactory(object):
    # field vars
    template_path = './js_templates.json'

    @staticmethod
    def init(template, setup_schema_loc):
        with open(setup_schema_loc, "r") as schema_file:
            schema_json = json.loads(schema_file.read())
        with open(template, "r") as template_file:
            template_json = json.loads(template_file.read())
        # Will need to do some processing here for other files that need to be read in
        return { 
            "template_json" : template_json,
            "schema_json" : schema_json
        }


    @staticmethod
    def generate_code(setup_schema_loc):
        template_inf = ScriptFactory.init(
                ScriptFactory.template_path, setup_schema_loc)
        print template_inf
        
        # Create views
            # bind logic to views
        pass

    class Form(object):
        def __init__(self, name, params, type):
            self.name = name
            self.params = params

ScriptFactory.generate_code('./test_setup.json')