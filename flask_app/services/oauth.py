from typing import Dict

import requests as requests
from flask import redirect

from config import google_config, BASE_HOST


class GoogleOauth:
    """Класс для работы с авторизацией гугла."""
    def __init__(self):
        self.client_id = google_config.client_id
        self.secret = google_config.secret
        self.redirect_url = f'{BASE_HOST}api/v1/oauth/google-redirect'
        self.scope = 'email profile openid'
        self.authorization_url = f'https://accounts.google.com/o/oauth2/auth?client_id={self.client_id}&' \
                                 f'scope={self.scope}&state=google' \
                                 f'access_type=offline&response_type=code&redirect_uri={self.redirect_url}&'

    def authorize(self):
        """Редирект на авторизацию в гугле."""
        return redirect(self.authorization_url, code=302)

    def get_tokens(self, code: str) -> Dict[str, str]:
        """Получить токены от гугла по коду."""
        return requests.post(
            url='https://oauth2.googleapis.com/token',
            data={
                'client_id': self.client_id,
                'client_secret': self.secret,
                'code': code,
                'redirect_uri': self.redirect_url,
                'grant_type': 'authorization_code',
            }
        ).json()

    def get_user_info(self, code: str) -> Dict[str, str]:
        """Получить информацию о юзере гугла по токенам."""
        tokens = self.get_tokens(code)
        return requests.get(
            url='https://www.googleapis.com/userinfo/v2/me',
            headers={'Authorization': f'{tokens["token_type"]} {tokens["access_token"]}'},
        ).json()
