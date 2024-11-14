from flask import request, make_response
import requests
from db import config
from functools import wraps

AUTH_URL = config.auth_url

def authenticate_user(email, password):
    response = requests.post(AUTH_URL, json={'email': email, 'password': password})
    if response.status_code == 200:
        auth_result = response.json()
        return auth_result == ["Verified", "True"]
    return False

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not authenticate_user(auth.username, auth.password):
            return make_response({'Error':'Authentication failed'}, 401)
        return f(*args, **kwargs)
    return decorated_function
