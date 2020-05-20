from werkzeug.security import safe_str_cmp
import requests

import bcrypt

from argparse import Namespace

def authenticate(username, password):
    user_resp = requests.get(f"http://user_service_proxy/users/{username}/_login")
    user = Namespace(**user_resp.json())
    if user and safe_str_cmp(user.password, bcrypt.hashpw(password.encode("utf-8"), user.password.encode("utf-8"))):
        return user


def identity(payload):
    user_handle = payload['identity']
    user_resp = requests.get(f"http://user_service_proxy/users/{user_handle}/_login")
    user = Namespace(user_resp.json())
    return user
