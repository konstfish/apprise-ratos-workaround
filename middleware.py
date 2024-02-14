from flask import request

import os
from dotenv import load_dotenv
load_dotenv()

def authorize_request():
    auth_key = request.args.get('key')
    key = os.environ.get('REQ_KEY')

    if key != None and auth_key != key:
        return {401: "unauthorized"}, 401