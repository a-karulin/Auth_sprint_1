from datetime import datetime
from typing import Dict, Type
import logging
import sqlalchemy.orm
from flask import abort
from sqlalchemy.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import engine, Base
from database.db_models import User, History, Roles, UsersRoles
from database.session_decorator import get_session


logger = logging.getLogger(__name__)


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
    ) -> Dict[str, str]:
        """Зарегистрировать пользователя."""
        logger.debug("Регистрация пользователя")
        try:
            session.query(User).filter(User.login == login).one()
            logger.info(f"Пользователь {login} уже существует")
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
            logger.info(f"Создан пользователь {login}")
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
    ) -> Dict[str, str]:
        """Получить пользователя по логину
        :param login: логин (e-mail пользователя)"""
        logger.debug(f"Вход пользователя {login} в учетную запись")
        try:
            user = session.query(User).filter(User.login == login).one()
            logger.info(f"Пользователь {login} найден")
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
                logger.info(f"В историю внесена информация о входе пользователя {login}")
                user = self._transform_query_to_dict(user)
                return user
            abort(401)

    @get_session()
    def change_password(
            self,
            user_id: str,
            old_password: str,
            new_password: str,
            session: sqlalchemy.orm.Session = None,
    ) -> Dict[str, str]:
        logger.debug(f"Меняем пароль для пользователя с ид {user_id}")
        try:
            user = session.query(User).filter(User.id == user_id).one()
            logger.info("Пользователь найден в бд")
        except NoResultFound:
            abort(404)
        else:
            if user and check_password_hash(user.password, old_password):
                user.password = generate_password_hash(new_password)
                session.commit()
                logger.info("Пароль пользователя изменен")
                user = session.query(User).filter(User.id == user_id).one()
                return user
            abort(401)

    @get_session()
    def change_login(
            self,
            user_id: str,
            password: str,
            new_login: str,
            session: sqlalchemy.orm.Session = None,
    ) -> Dict[str, str]:
        logger.debug(f"Меняем e-mail для пользователя с ид {user_id}")
        try:
            user = session.query(User).filter(User.id == user_id).one()
            logger.info("Пользователь найден в бд")
        except NoResultFound:
            abort(404)
        else:
            if user and check_password_hash(user.password, password):
                user.login = new_login
                session.commit()
                logger.info("Логин пользователя изменен")
                user = session.query(User).filter(User.id == user_id).one()
                return user
            abort(401)

    @get_session()
    def get_login_history(
            self,
            user_id: str,
            session: sqlalchemy.orm.Session = None,
    ) -> Dict[str, str]:
        logger.debug(f"Получаем историю по пользователю с ид {user_id}")
        query = session.query(History).filter(History.user_id == user_id).all()
        result = dict()
        for row in query:
            result[str(row.auth_date)] = row.user_agent
        return result

    @get_session()
    def get_user_by_id(
            self,
            user_id: str,
            session: sqlalchemy.orm.Session = None,
    ) -> Dict[str, str]:
        logger.debug(f"Получаем полную информацию по пользователю по ид {user_id}")
        try:
            user = session.query(User).filter(User.id == user_id).one()
        except NoResultFound:
            abort(404)
        else:
            return self._transform_query_to_dict(user)

    @get_session()
    def get_roles_names_for_user(self, user_id: str, session: sqlalchemy.orm.Session = None):
        logger.debug("Получаем роли по пользователю")
        roles = session.query(
            Roles.role,
        ).join(
            UsersRoles,
            Roles.id == UsersRoles.role_id,
        ).where(
            UsersRoles.user_id == user_id,
        ).all()
        roles = [role.role for role in roles]
        return roles

    @staticmethod
    def _transform_query_to_dict(row: Type[Base]) -> Dict[str, str]:
        query_as_dict = {}
        for column in row.__table__.columns:
            if column.name != 'password':
                query_as_dict[column.name] = getattr(row, column.name)
        return query_as_dict

    @get_session()
    def create_superuser(
            self,
            password: str,
            login: str,
            first_name: str,
            last_name: str,
            session: sqlalchemy.orm.Session = None
    ):
        logger.debug("Создаем админа")
        try:
            session.query(User).filter(User.login == login).one()
            logger.debug("Админ уже существует")
        except NoResultFound:
            password_hash = generate_password_hash(password)
            admin = User(
                login=login,
                password=password_hash,
                first_name=first_name,
                last_name=last_name,
                is_admin=True
            )
            session.add(admin)
            session.commit()
            logger.debug("Админ создан")
            new_user = session.query(User).filter(User.login == login).one()
            new_user = self._transform_query_to_dict(new_user)
            return new_user
        else:
            abort(400)


user_service = UserService()
