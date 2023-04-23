from http import HTTPStatus

from flask import Blueprint, request, jsonify, make_response

from services.tokens import create_access_and_refresh_tokens
from services.user import UserService

auth = Blueprint("auth", __name__)


@auth.errorhandler(404)
def handle_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), HTTPStatus.NOT_FOUND)


@auth.errorhandler(400)
def handle_bad_request(error):
    return make_response(jsonify({'error': 'No result found'}), HTTPStatus.NOT_FOUND)


@auth.errorhandler(403)
def handle_non_authorized_request(error):
    return make_response(jsonify({'error': 'Not authorized'}), HTTPStatus.NOT_FOUND)


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


@auth.route("/logout")
def logout():
    pass


@auth.route("/refresh", methods=["POST"])
def refresh_tokens():
    pass


@auth.route("/update-data", methods=["POST"])
def update_data():
    pass
