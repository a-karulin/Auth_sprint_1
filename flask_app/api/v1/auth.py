import datetime
from http import HTTPStatus

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from database.db import db_session
from database.db_models import User, History
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def create_user():
    pass


@auth.route("/login", methods=["POST"])
def login_user(login: str, password: str):
    user = db_session.query(User).filter(User.login == login).first()
    if not user:
        return HTTPStatus.NOT_FOUND
    user_id = str(user.id)
    user_agent = request.headers.get("user-agent", "")
    user_info = History(
        user_id=user_id,
        user_agent=user_agent,
        auth_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    hash = generate_password_hash(password)
    if check_password_hash(hash, user.password):
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        db_session.session.add(user_info)
        db_session.session.commit()
        db_session.session.remove()
        return jsonify(
            {
                "message": "Successful Login",
                "user": user_id,
                "access_token": access_token.decode("utf-8"),
                "refresh_token": refresh_token.decode("utf-8"),
            })
    return jsonify({"message": "Wrong password"})


@auth.route("/logout")
def logout():
    pass


@auth.route("/refresh", methods=["POST"])
def refresh_token():
    pass


@auth.route("/update-data", methods=["POST"])
def update_data():
    pass
