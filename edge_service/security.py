from flask import current_app

import jwt

import requests
import datetime
import bcrypt

from argparse import Namespace


def identity(payload):
    user_handle = payload['identity']
    user_resp = requests.get(f"http://user_service_proxy/users/{user_handle}/_login")
    user = Namespace(user_resp.json())
    return user

class AuthHandle:
    def __init__(self, request):
        self.request = request
        self.app = current_app

    def __call__(self):
        data = self.request.get_json()
        user = self.authenticate(**data)
        return self.encode_auth_token(user)

    def authenticate(self, username, password):
        user_resp = requests.get(f"http://user_service_proxy/users/{username}/_login")

        try:
            user = Namespace(**user_resp.json())
        except Exception:
            raise ValueError(f"No such user: {username}")

        if user and bcrypt.checkpw(user.password.encode("utf-8"), password.encode("utf-8")):
            return user

    def encode_auth_token(self, user):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=10),
                'iat': datetime.datetime.utcnow(),
                'sub': user.handle,
                'role': user.role
            }
            return jwt.encode(
                payload,
                self.app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def requires_auth(func):
        def __inner(*args, **kwargs):
            ret = func(*args, **kwargs)
            return ret
        return __inner
