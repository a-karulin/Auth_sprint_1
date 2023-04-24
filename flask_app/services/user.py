from datetime import datetime

import sqlalchemy.orm
from flask import abort
from sqlalchemy.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import engine
from database.db_models import User, History, Roles, UsersRoles
from database.session_decorator import get_session
from typing import Union


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
            return new_user.id
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

                return user.id
            abort(403)

    @get_session()
    def get_user(
            self,
            user_data: Union[str, int],
            session: sqlalchemy.orm.Session = None
    ):
        try:
            if isinstance(user_data, str):
                user = session.query(User).filter(login=user_data).one()
            else:
                user = session.query(User).filter(id=user_data).one()
            return user
        except NoResultFound:
            abort(404)

    @get_session()
    def apply_user_role(
            self,
            user_id,
            role: Roles,
            session: sqlalchemy.orm.Session = None
    ):
        user_role = session.query(UsersRoles).filter(user_id=user_id, role_id=role.id).first()
        if user_role:
            return {"msg": "User has this role"}
        new_user_role = UsersRoles(user_id=user_id, role_id=role.id)
        session.add(new_user_role)
        session.commit()
        return {"msg": "Applied role for user"}

    @get_session()
    def delete_user_role(
            self,
            user_id,
            role: Roles,
            session: sqlalchemy.orm.Session = None
    ):
        user_role = session.query(UsersRoles).filter(user_id=user_id, role_id=role.id).first()
        if not user_role:
            return {"msg": "User doesn't have this role"}
        new_user_role = UsersRoles(user_id=user_id, role_id=role.id)
        session.add(new_user_role)
        session.commit()
        return {"msg": "Deleted role for user"}

    def get_login_history(self, user_id, session: sqlalchemy.orm.Session = None):
        query = session.query(History).filter(History.user_id == user_id).all()
        result = dict()
        for row in query:
            result[str(row.auth_date)] = row.user_agent
        return result

    def logout_user(self):
        pass
