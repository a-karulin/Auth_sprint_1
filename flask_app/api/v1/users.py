from http import HTTPStatus

from flask import Blueprint, jsonify
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
    user_id = token.get('sub')
    user_service = UserService()
    return jsonify(
        {'history': [user_service.get_login_history(user_id)]}
    ), HTTPStatus.OK
