import datetime
from http import HTTPStatus

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from services.history import HistoryService
from services.tokens import create_access_and_refresh_tokens
from services.user import UserService

auth = Blueprint("auth", __name__)


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
    login = request.json.get('login')
    password = request.json.get('password', None)
    user_service = UserService()
    user = user_service.get_user(login)
    if not user:
        return HTTPStatus.NOT_FOUND
    user_id = str(user.id)

    if check_password_hash(user.password, password):
        access_token, refresh_token = create_access_and_refresh_tokens({'user_id': user_id})
        history_service = HistoryService()
        history_service.create_history_record(
            user_id=user_id,
            user_agent=request.headers.get("user-agent", ""),
        )
        return jsonify(
            {
                "message": "Successful Login",
                "user": user_id,
                "access_token": access_token,
                "refresh_token": refresh_token,
            })
    return jsonify({"message": "Wrong password"})


@auth.route("/logout")
def logout():
    pass


@auth.route("/refresh", methods=["POST"])
def refresh_tokens():
    pass


@auth.route("/update-data", methods=["POST"])
def update_data():
    pass
