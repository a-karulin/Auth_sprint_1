import sqlalchemy.orm

from database.db import engine
from database.db_models import User
from database.session_decorator import get_session


class UserService:
    def __init__(self):
        self.engine = engine

    @get_session()
    def register_user(
            self,
            password: str,
            login: str,
            first_name: str,
            last_name: str,
            session: sqlalchemy.orm.Session = None
    ):
        user = None
        try:
            user = session.query(User).filter(User.login == login).one()
        except Exception:
            pass
        return user
