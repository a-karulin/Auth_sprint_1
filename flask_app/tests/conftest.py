import pytest
from sqlalchemy.orm import Session

from database.db import engine
from database.db_models import User

HOST = 'http://auth_service:5000'


@pytest.fixture()
def delete_user_after_test():
    with Session(engine) as session:
        yield
        session.query(User).filter_by(login='test_login').delete()
        session.commit()
