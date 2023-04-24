from http import HTTPStatus

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from database.db_models import User, Roles
from services.role import RoleService
from services.user import UserService

users = Blueprint("users", __name__)


@users.route("/roles", methods=["GET"])
def get_user_roles():
    identity = get_jwt_identity()
    user_service = UserService()
    user = user_service.get_user(identity)
    return [Roles(name=role.name) for role in user.roles]


@users.route("/{user_id}/apply-roles", methods=["POST"])
def apply_roles():
    role_service = RoleService()
    role = role_service.get_role(request.json.get('role_name'))
    user_service = UserService()
    user_id = request.args.get('user_id')
    response = user_service.apply_user_role(user_id, role)

    return jsonify(response), HTTPStatus.OK


@users.route("/{user_id}/delete_role", methods=["DELETE"])
def delete_user_from_role():
    role_service = RoleService()
    role = role_service.get_role(request.json.get('role_name'))
    user_service = UserService()
    user_id = request.args.get('user_id')
    response = user_service.delete_user_role(user_id, role)

    return jsonify(response), HTTPStatus.OK


@users.route("/{user_id}/roles", methods=["GET"])
def get_user_history():
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
