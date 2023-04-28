from http import HTTPStatus

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from services.role import RoleService
from services.tokens import admin_access, validate_access_token
from services.user import UserService

users = Blueprint("users", __name__)


@users.route("/apply-role", methods=["POST"])
@admin_access()
@jwt_required()
@validate_access_token()
def apply_role_to_user():
    role_service = RoleService()
    role_service.apply_user_role(
        user_id=request.json.get('user_id'),
        role_id=request.json.get('role_id'),
    )

    return jsonify({'msg': 'role created'}), HTTPStatus.OK


@users.route("/delete-role", methods=["DELETE"])
@admin_access()
@jwt_required()
@validate_access_token()
def delete_role_from_user():
    role_service = RoleService()
    role_service.delete_user_role(
        user_id=request.json.get('user_id'),
        role_id=request.json.get('role_id'),
    )

    return jsonify({'msg': 'role deleted'}), HTTPStatus.OK


@users.route("/{user_id}/roles", methods=["GET"])
def get_user_history():
    pass


@users.route("/login-history", methods=["GET"])
@jwt_required()
@validate_access_token()
def get_login_history():
    token = get_jwt()
    user_id = token.get('sub')
    user_service = UserService()
    return jsonify(
        {'history': [user_service.get_login_history(user_id)]}
    ), HTTPStatus.OK


@users.route("/change-password", methods=["POST"])
@jwt_required()
@validate_access_token()
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
@validate_access_token()
def change_login():
    token = get_jwt()
    user_service = UserService()
    user_service.change_login(
        user_id=token.get('sub'),  # TODO: add payload
        new_login=request.json.get('new_login'),
        password=request.json.get('password'),
    )
    return jsonify({'msg': 'login updated'}), HTTPStatus.OK
