from http import HTTPStatus

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from services.role import RoleService
from services.tokens import admin_access

roles = Blueprint("roles", __name__)


@roles.route("/", methods=["GET"])
@jwt_required()
@admin_access()
def roles_list():
    role_service = RoleService()
    roles = role_service.get_all_roles()
    return roles, HTTPStatus.OK


@roles.route("/create", methods=["POST"])
@jwt_required()
@admin_access()
def create_role():
    role_service = RoleService()
    role_service.create_role(request.json.get('role'))
    return jsonify({"msg": "Created new role"}), HTTPStatus.CREATED


@roles.route("/<role_id>", methods=["PATCH"])
@admin_access()
def update_role(role_id):
    new_role_name = request.json.get('role')
    role_service = RoleService()
    role_service.update_role(role_id, new_role_name)
    return jsonify({"msg": "Updated role"}), HTTPStatus.CREATED


@roles.route("/<role_id>", methods=["DELETE"])
@admin_access()
def delete_role(role_id):
    role_service = RoleService()
    role_service.delete_role(role_id)
    return jsonify({"msg": "Deleted role"}), HTTPStatus.OK
