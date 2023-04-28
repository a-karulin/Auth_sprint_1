from datetime import datetime

import sqlalchemy.orm
from flask import abort
from sqlalchemy.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import engine
from database.db_models import User, History
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
            new_user = self._transform_query_to_dict(new_user)
            return new_user
        else:
            abort(400)

    @get_session()
    def login_user(
            self,
            login: str,
            password: str,
            user_agent: str,
            session: sqlalchemy.orm.Session = None
    ):
        """Получить пользователя по логину
        :param login: логин (e-mail пользователя)"""

        try:
            user = session.query(User).filter(User.login == login).one()
        except NoResultFound:
            abort(404)
        else:
            if check_password_hash(user.password, password):
                user_info = History(
                    user_id=user.id,
                    user_agent=user_agent,
                    auth_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M")
                )
                session.add(user_info)
                session.commit()

                user = self._transform_query_to_dict(user)
                return user
            abort(403)

    @get_session()
    def change_password(
            self,
            user_id,
            old_password,
            new_password,
            session: sqlalchemy.orm.Session = None,
    ):
        try:
            user = session.query(User).filter(User.id == user_id).one()
        except NoResultFound:
            abort(404)
        else:
            if user and check_password_hash(user.password, old_password):
                user.password = generate_password_hash(new_password)
                session.commit()
                user = session.query(User).filter(User.id == user_id).one()
                return user
            abort(401)

    @get_session()
    def change_login(
            self,
            user_id,
            password,
            new_login,
            session: sqlalchemy.orm.Session = None,
    ):
        try:
            user = session.query(User).filter(User.id == user_id).one()
        except NoResultFound:
            abort(404)
        else:
            if user and check_password_hash(user.password, password):
                user.login = new_login
                session.commit()
                user = session.query(User).filter(User.id == user_id).one()
                return user
            abort(401)

    @staticmethod
    def _transform_query_to_dict(row) -> dict:
        query_as_dict = {}
        for column in row.__table__.columns:
            if column.name != 'password':
                query_as_dict[column.name] = getattr(row, column.name)
        return query_as_dict
