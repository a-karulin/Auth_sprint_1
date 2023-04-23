from datetime import timedelta

import redis
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token

from config import redis_config


def create_access_and_refresh_tokens(identity, seconds=900, days=30):
    exp_access = timedelta(seconds=seconds)
    exp_refresh = timedelta(days=days)
    access_token = create_access_token(
        identity=identity, expires_delta=exp_access)
    refresh_token = create_refresh_token(
        identity=identity, expires_delta=exp_refresh)

    return access_token, refresh_token


class RedisTokenStorage:
    def __init__(self):
        self.redis_host = redis_config.host
        self.redis_port = redis_config.port
        self.jwt_redis_blocklist = redis.StrictRedis(
            host=self.redis_host, port=self.redis_port, db=0, decode_responses=True
        )

    def add_refresh_token_to_blocklist(self, token):
        jti = token["jti"]
        iat = token.get('iat')
        exp = token.get('exp')
        seconds_till_expire = exp - iat
        self.jwt_redis_blocklist.set(jti, "", ex=timedelta(seconds=seconds_till_expire))

    def check_token_in_blacklist(self, token):
        jti = token["jti"]
        return self.jwt_redis_blocklist.get(jti)
