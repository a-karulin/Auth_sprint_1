from flask import redirect

from config import google_config


class GoogleOauth:
    def __init__(self):
        self.client_id = google_config.client_id
        self.secret = google_config.secret
        self.redirect_url = None
        self.scope = 'email profile openid'
        self.authorization_url = 'https://accounts.google.com/o/oauth2/auth?client_id={self.client_id}&' \
                                 f'scope={self.scope}&state=google' \
                                 f'access_type=offline&response_type=code&redirect_uri={self.redirect_url}&'

    def authorize(self):
        return redirect(self.authorization_url, code=302)
