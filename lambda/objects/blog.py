import uuid

class blog(object):
    def __init__(self, title = None, description= None, *args, **kwargs):
        if title is None or title == "":
            raise ValueError ("title should not be empty or null")
        if description is None:
            raise ValueError ("description should not be null")

        self.ID = str(uuid.uuid4())
        self.TITLE = title
        self.DESCRIPTION = description

# import json
# j = json.loads('{"title":"a","description": "John Smith", "username": "jsmith", "hello": "world"}')
# u = blog(**j)
# print(json.dumps(u.__dict__))