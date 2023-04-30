import requests

from tests.conftest import HOST


def test_create_role(get_tokens_for_admin):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f'Bearer {get_tokens_for_admin["access_token"]}',
    }
    data = {'role': 'test_role'}
    url = f'{HOST}/api/v1/roles/create'
    response = requests.post(
        url=url,
        json=data,
        headers=headers,
    )
    assert response.status_code == 201


def test_create_role_not_admin(get_tokens):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f'Bearer {get_tokens["access_token"]}',
    }
    data = {'role': 'test_role'}
    url = f'{HOST}/api/v1/roles/create'
    response = requests.post(
        url=url,
        json=data,
        headers=headers,
    )
    assert response.status_code == 403
