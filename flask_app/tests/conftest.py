import pytest
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from database.db import engine
from database.db_models import User

HOST = 'http://auth_service:5000'
TEST_LOGIN = 'test_login'
TEST_PASSWORD = 'test_password'
TEST_FIRST_NAME = 'test_first_name'
TEST_LAST_NAME = 'test_last_name'


@pytest.fixture()
def delete_user_after_test():
    with Session(engine) as session:
        yield
        session.query(User).filter_by(login=TEST_LOGIN).delete()
        session.commit()


@pytest.fixture()
def create_and_delete_user():
    with Session(engine) as session:
        new_user = User(
            login=TEST_LOGIN,
            password=generate_password_hash(TEST_PASSWORD),
            first_name=TEST_FIRST_NAME,
            last_name=TEST_LAST_NAME,
        )
        session.add(new_user)
        session.commit()
        yield
        session.query(User).filter_by(login=TEST_LOGIN).delete()
        session.commit()
