from datetime import timedelta

from flask_jwt_extended import get_jwt, jwt_required, get_current_user
import redis
from http import HTTPStatus

from flask import Blueprint, request, jsonify

from services.tokens import create_access_and_refresh_tokens
from services.user import UserService

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
    db = UserService()
    new_user = db.register_user(
        login=request.json.get('login'),
        password=request.json.get('password'),
        last_name=request.json.get('last_name'),
        first_name=request.json.get('first_name'),
    )
    access_token, refresh_token = create_access_and_refresh_tokens(new_user)
    response = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'id': new_user,
    }
    return jsonify(response), HTTPStatus.CREATED


@auth.route("/login", methods=["POST"])
def login_user():
    user_service = UserService()
    user = user_service.login_user(
        login=request.json.get('login'),
        password=request.json.get('password', None),
        user_agent=request.headers.get("user-agent", ""),
    )
    access_token, refresh_token = create_access_and_refresh_tokens(user)
    response = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'id': user,
    }
    return jsonify(response), HTTPStatus.OK


@auth.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    response = {'msg': f"{ttype.capitalize()} token successfully revoked"}

    # Returns "Access token revoked" or "Refresh token revoked"
    return jsonify(response), HTTPStatus.OK


@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_tokens():
    user = get_current_user()
    user_id = user.id
    token = get_jwt()
    jti = token["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    access_token, refresh_token = create_access_and_refresh_tokens(user_id)
    response = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'id': user_id,
    }
    return jsonify(response), HTTPStatus.OK


@auth.route("/update-data", methods=["POST"])
def update_data():
    pass
