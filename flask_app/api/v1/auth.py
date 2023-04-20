from http import HTTPStatus

from flask import Blueprint, request, jsonify

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
        id: new_user,
    }
    return jsonify(response), HTTPStatus.CREATED


@auth.route("/login", methods=["POST"])
def login_user():
    pass


@auth.route("/logout")
def logout():
    pass


@auth.route("/refresh", methods=["POST"])
def refresh_token():
    pass


@auth.route("/update-data", methods=["POST"])
def update_data():
    pass
