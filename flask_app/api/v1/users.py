from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from database.db_models import User, Roles
from services.role import RoleService
from services.user import UserService

users = Blueprint("users", __name__)


@users.route("/roles", methods=["GET"])
def get_user_roles():
    identity = get_jwt_identity()
    user_service = UserService()
    user = user_service.get_user(user_id=identity)
    return [Roles(name=role.name) for role in user.roles]


@users.route("/apply-roles", methods=["POST"])
def apply_roles():
    role_service = RoleService()
    role = role_service.get_role(request.json.get('role_name'))
    identity = get_jwt_identity()
    user_service = UserService()
    user_service.apply_user_role(identity, role)

    new_role_user = UserRole(user_id=body.user_id, role_id=body.role_id)
    db.session.add(new_role_user)
    db.session.commit()
    return {"msg": "Role is assigned to the user"}, HTTPStatus.CREATED


@users.route("/{user_id}/delete_role", methods=["DELETE"])
def delete_user_from_role():
    pass


@users.route("/{user_id}/roles", methods=["GET"])
def get_user_history():
    pass
