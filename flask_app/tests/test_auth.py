from random import randint

import requests

from tests.conftest import HOST


def test_sign_up(delete_user_after_test):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = f'{HOST}/api/v1/auth/signup'
    data = {'login': 'test_login', 'password': str(randint(0, 10000)),
            'first_name': 'test_first_name', 'last_name': 'test_last_name'}
    response = requests.post(url=url,
                             json=data,
                             headers=headers
                             )
    assert response.status_code == 201
