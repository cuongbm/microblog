from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User, Token
from app.api.errors import error_response

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)


token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verify_token(token):
    tk = Token.check(token)
    g.current_user = tk.user if tk else None
    g.current_token = tk
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return error_response(401)
