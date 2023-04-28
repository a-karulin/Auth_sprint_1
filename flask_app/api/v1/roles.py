from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from database.db_models import Roles
from services.role import RoleService
from services.tokens import admin_access

roles = Blueprint("roles", __name__)


@roles.route("/", methods=["GET"])
@jwt_required()
@admin_access()
def roles_list():
    return [Roles(id=role_item.id, role=role_item.role) for role_item in Roles.query.all()]


@roles.route("/create", methods=["POST"])
@jwt_required()
@admin_access()
def create_role():
    role_service = RoleService()
    response, http_status = role_service.create_role(request.json.get('role'))
    return jsonify(response), http_status


@roles.route("/<role_id>", methods=["PATCH"])
@admin_access()
def update_role():
    role_id = request.args.get('user_id')
    new_role_name = request.json.get('role')
    role_service = RoleService()
    response, http_status = role_service.update_role(role_id, new_role_name)
    return jsonify(response), http_status


@roles.route("/<role_id>", methods=["DELETE"])
@admin_access()
def delete_role():
    role_id = request.args.get('user_id')
    role_service = RoleService()
    response, http_status = role_service.delete_role(role_id)
    return jsonify(response), http_status
