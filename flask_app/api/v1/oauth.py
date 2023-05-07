from flask import Blueprint

from services.oauth import GoogleOauth

oauth = Blueprint('oauth', __name__)


@oauth.route("/google", methods=["GET"])
def authorize_with_google():
    google = GoogleOauth()
    return google.authorize()
