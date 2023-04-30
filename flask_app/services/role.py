from typing import List, Dict, Type
import logging
import sqlalchemy.orm
from flask import abort
from sqlalchemy.exc import NoResultFound, DataError

from database.db import engine, Base
from database.db_models import Roles, UsersRoles
from database.session_decorator import get_session

logger = logging.getLogger(__name__)


class RoleService:
    def __init__(self):
        self.engine = engine

    @get_session()
    def get_all_roles(self, session: sqlalchemy.orm.Session = None) -> List[Dict[str, str]]:
        logger.debug("Получаем список всех ролей")
        try:
            roles = session.query(Roles).all()
            logger.info("Список ролей получен")
        except NoResultFound:
            abort(404)
        else:
            if roles:
                roles = [
                    self._transform_query_to_dict(role) for role in roles
                ]
            return roles

    @get_session()
    def apply_user_role(
            self,
            user_id: str,
            role_id: str,
            session: sqlalchemy.orm.Session = None,
    ) -> None:
        logger.debug(f"Применяем роль с ид {role_id} для пользователя с ид {user_id}")
        try:
            session.query(UsersRoles).filter(
                UsersRoles.user_id == user_id,
                UsersRoles.role_id == role_id,
            ).one()
            logger.info(f"Роль с ид {role_id} уже есть у пользователя с ид {user_id}")
        except NoResultFound:
            new_role = UsersRoles(user_id=user_id, role_id=role_id)
            session.add(new_role)
            session.commit()
            logger.info(f"Применена роль с ид {role_id} для пользователя с ид {user_id}")
        else:
            abort(409)

    @get_session()
    def delete_user_role(
            self,
            user_id: str,
            role_id: str,
            session: sqlalchemy.orm.Session = None
    ) -> None:
        logger.debug(f"Удаляем роль с ид {role_id} у пользователя с ид {user_id}")
        try:
            role = session.query(UsersRoles).filter(
                UsersRoles.user_id == user_id,
                UsersRoles.role_id == role_id,
            ).one()
            session.delete(role)
            session.commit()
            logger.info(f"Удалена роль с ид {role_id} для пользователя с ид {user_id}")
        except NoResultFound:
            abort(404)

    @get_session()
    def create_role(
            self,
            role_name: str,
            session: sqlalchemy.orm.Session = None
    ) -> None:
        logger.debug(f"Создаем роль с названием {role_name}")
        if session.query(Roles).filter(Roles.role == role_name).first():
            abort(409)
        role = Roles(role=role_name)
        session.add(role)
        session.commit()
        logger.info(f"Роль {role_name} записана в бд")
        return role

    @get_session()
    def update_role(
            self,
            role_id: str,
            role_name: str,
            session: sqlalchemy.orm.Session = None
    ) -> None:
        logger.debug(f"Обновляем информацию по роли с ид {role_id}")
        try:
            session.query(Roles).filter_by(id=role_id).update({"role": role_name})
        except DataError:
            abort(404)
        session.commit()
        logger.info(f"Информация по роли с ид {role_id} обновлена")

    @get_session()
    def delete_role(
            self,
            role_id: str,
            session: sqlalchemy.orm.Session = None
    ) -> None:
        logger.debug(f"Удаляем роль с ид {role_id}")
        session.query(Roles).filter_by(id=role_id).delete()
        session.commit()
        logger.debug(f"роль с ид {role_id} удалена")

    @staticmethod
    def _transform_query_to_dict(row: Type[Base]) -> Dict[str, str]:
        query_as_dict = {}
        for column in row.__table__.columns:
            query_as_dict[column.name] = getattr(row, column.name)
        return query_as_dict


role_service = RoleService()
