from flask import Blueprint

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def create_user():
    pass


@auth.route("/login", methods=["POST"])
def login_user():
    pass


@auth.route("/logout")
def logout():
    pass


@auth.route("/refresh", methods=["POST"])
def refresh_token():
    pass


@auth.route("/change-password", methods=["POST"])
def change_password():
    pass
