from flask import Blueprint, request

from services.user import UserService

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def create_user():
    db = UserService()
    return db.register_user(
        login=request.json.get('login'),
        password=request.json.get('password'),
        last_name=request.json.get('password'),
        first_name=request.json.get('password'),
    )


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
