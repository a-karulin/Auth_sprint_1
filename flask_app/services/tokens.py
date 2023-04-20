from datetime import timedelta

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token


def create_access_and_refresh_tokens(identity):
    exp_access = timedelta(minutes=15)
    exp_refresh = timedelta(days=30)
    access_token = create_access_token(
        identity=identity, expires_delta=exp_access)
    refresh_token = create_refresh_token(
        identity=identity, expires_delta=exp_refresh)

    return access_token, refresh_token
