from datetime import timedelta

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, jwt_required
import redis

auth = Blueprint("auth", __name__)

# Setup our redis connection for storing the blocklisted tokens. You will probably
# want your redis instance configured to persist data to disk, so that a restart
# does not cause your application to forget that a JWT was revoked.
jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

ACCESS_EXPIRES = timedelta(hours=1)


@auth.route("/signup", methods=["POST"])
def create_user():
    pass


@auth.route("/login", methods=["POST"])
def login_user():
    pass


@auth.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

    # Returns "Access token revoked" or "Refresh token revoked"
    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")


@auth.route("/refresh", methods=["POST"])
def refresh_token():
    pass


@auth.route("/update-data", methods=["POST"])
def update_data():
    pass
