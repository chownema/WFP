import json
import date_time_encoder

class common_response(object):
    """
    Object class for response

    Params
    @status code: status code of the functions
    @headers : header to be returned
    @body : body to be response

    Return :  a response object with the body in JSON

    """

    def __init__(self, status_code = None, headers= None, body = None, *args, **kwargs):
        self.status_code = status_code
        self.headers = headers
        self.body = json.dumps(body, cls=date_time_encoder.DateTimeEncoder)

