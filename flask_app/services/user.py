import sqlalchemy.orm
from flask import abort
from sqlalchemy.exc import NoResultFound
from werkzeug.security import generate_password_hash

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
        try:
            session.query(User).filter(User.login == login).one()
        except NoResultFound:
            password_hash = generate_password_hash(password)
            new_user = User(
                login=login,
                password=password_hash,
                first_name=first_name,
                last_name=last_name,
            )
            session.add(new_user)
            session.commit()
            new_user = session.query(User).filter(User.login == login).one()
            return {'user_id': new_user.id}
        else:
            abort(400)

    @get_session()
    def get_user(
            self,
            login,
            session: sqlalchemy.orm.Session = None
    ):
        """Получить пользователя по логину
        :param login: логин (e-mail пользователя)"""
        return session.query(User).filter(User.login == login).one()
