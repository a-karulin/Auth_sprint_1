from flask import Blueprint

users = Blueprint("users", __name__)


@users.route("/{user_id}/roles", methods=["GET"])
def get_user_roles():
    pass


@users.route("/{user_id}/apply-roles", methods=["POST"])
def apply_roles():
    pass


@users.route("/{user_id}/delete_role", methods=["DELETE"])
def delete_role_from_user():
    pass
