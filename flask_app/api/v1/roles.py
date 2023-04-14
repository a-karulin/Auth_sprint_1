from flask import Blueprint


roles = Blueprint("roles", __name__)


@roles.route("/", methods=["GET"])
def roles_list():
    pass


@roles.route("/", methods=["POST"])
def create_role():
    pass


@roles.route("/<role_id>", methods=["POST"])
def update_role():
    pass


@roles.route("/<role_id>", methods=["DELETE"])
def delete_role():
    pass
