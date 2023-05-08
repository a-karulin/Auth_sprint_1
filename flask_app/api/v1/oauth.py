from flask import Blueprint, request, jsonify

from services.oauth import GoogleOauth

oauth = Blueprint('oauth', __name__)


@oauth.route("/google", methods=["GET"])
def authorize_with_google():
    google = GoogleOauth()
    return google.authorize()


@oauth.route('/google-redirect', methods=['GET'])
def callback_google():
    code = request.args.get('code')
    google = GoogleOauth()
    user_info = google.get_user_info(code)
    return jsonify({'user_info': user_info})
