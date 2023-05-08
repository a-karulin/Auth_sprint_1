from http import HTTPStatus

from flask import Blueprint, request, jsonify

from services.oauth import GoogleOauth
from services.tokens import create_access_and_refresh_tokens
from services.user import user_service

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
    user = user_service.register_user_oauth(
        user_agent=request.headers.get('user-agent', ''),
        email=user_info['email'],
        oauth_id=user_info['id'],
        oauth_first_name=user_info['given_name'],
        oauth_last_name=user_info['family_name'],
    )
    access_token, refresh_token = create_access_and_refresh_tokens(
        identity=user['id'],
        payload=user,
    )
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user,
    }), HTTPStatus.OK
