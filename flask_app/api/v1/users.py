from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from services.user import UserService

users = Blueprint("users", __name__)


@users.route("/{user_id}/roles", methods=["GET"])
def get_user_roles():
    pass


@users.route("/{user_id}/apply-roles", methods=["POST"])
def apply_roles():
    pass


@users.route("/{user_id}/delete_role", methods=["DELETE"])
def delete_user_from_role():
    pass


@users.route("/login-history", methods=["GET"])
@jwt_required()
def get_login_history():
    token = get_jwt()
    user_id = token.get('sub')  # TODO: add payload
    user_service = UserService()
    return jsonify(
        {'history': [user_service.get_login_history(user_id)]}
    ), HTTPStatus.OK


@users.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    token = get_jwt()
    user_service = UserService()
    user_id = token.get('sub')  # TODO: add payload
    user_service.change_password(
        user_id=user_id,
        old_password=request.json.get('old_password'),
        new_password=request.json.get('new_password'),
    )
    return jsonify({'msg': 'password updated'}), HTTPStatus.OK
