from http import HTTPStatus

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from database.db_models import Roles
from services.role import RoleService
from services.tokens import admin_access
from services.user import UserService

users = Blueprint("users", __name__)


@users.route("/roles", methods=["GET"])
@jwt_required()
def get_user_roles():
    identity = get_jwt_identity()
    user_service = UserService()
    user = user_service.get_user(identity)
    roles = user_service.get_roles_of_user(user)
    return jsonify({'roles': roles}), HTTPStatus.OK


@users.route("/apply-role", methods=["POST"])
@admin_access()
@jwt_required()
def apply_role():
    role_service = RoleService()
    response = role_service.apply_user_role(
        user_id=request.json.get('user_id'),
        role_id=request.json.get('role_id'),
    )

    return jsonify(response), HTTPStatus.OK


@users.route("/{user_id}/delete_role", methods=["DELETE"])
@jwt_required()
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
    user_service.change_password(
        user_id=token.get('sub'),  # TODO: add payload,
        old_password=request.json.get('old_password'),
        new_password=request.json.get('new_password'),
    )
    return jsonify({'msg': 'password updated'}), HTTPStatus.OK


@users.route("/change-login", methods=["POST"])
@jwt_required()
def change_login():
    token = get_jwt()
    user_service = UserService()
    user_service.change_login(
        user_id=token.get('sub'),  # TODO: add payload
        new_login=request.json.get('new_login'),
        password=request.json.get('password'),
    )
    return jsonify({'msg': 'login updated'}), HTTPStatus.OK
