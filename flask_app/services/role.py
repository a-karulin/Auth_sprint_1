from typing import List, Dict, Type

import sqlalchemy.orm
from flask import abort
from sqlalchemy.exc import NoResultFound, DataError

from database.db import engine, Base
from database.db_models import Roles, UsersRoles
from database.session_decorator import get_session


class RoleService:
    def __init__(self):
        self.engine = engine

    @get_session()
    def get_all_roles(self, session: sqlalchemy.orm.Session = None) -> List[Dict[str, str]]:
        try:
            roles = session.query(Roles).all()
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
        try:
            session.query(UsersRoles).filter(
                UsersRoles.user_id == user_id,
                UsersRoles.role_id == role_id,
            ).one()
        except NoResultFound:
            new_role = UsersRoles(user_id=user_id, role_id=role_id)
            session.add(new_role)
            session.commit()
        else:
            abort(409)

    @get_session()
    def delete_user_role(
            self,
            user_id: str,
            role_id: str,
            session: sqlalchemy.orm.Session = None
    ) -> None:
        try:
            role = session.query(UsersRoles).filter(
                UsersRoles.user_id == user_id,
                UsersRoles.role_id == role_id,
            ).one()
            session.delete(role)
            session.commit()
        except NoResultFound:
            abort(404)

    @get_session()
    def create_role(
            self,
            role_name: str,
            session: sqlalchemy.orm.Session = None
    ) -> None:
        if session.query(Roles).filter(Roles.role == role_name).first():
            abort(409)
        role = Roles(role=role_name)
        session.add(role)
        session.commit()
        return role

    @get_session()
    def update_role(
            self,
            role_id: str,
            role_name: str,
            session: sqlalchemy.orm.Session = None
    ) -> None:
        try:
            session.query(Roles).filter_by(id=role_id).update({"role": role_name})
        except DataError:
            abort(404)
        session.commit()

    @get_session()
    def delete_role(
            self,
            role_id: str,
            session: sqlalchemy.orm.Session = None
    ) -> None:
        session.query(Roles).filter_by(id=role_id).delete()
        session.commit()

    @staticmethod
    def _transform_query_to_dict(row: Type[Base]) -> Dict[str, str]:
        query_as_dict = {}
        for column in row.__table__.columns:
            query_as_dict[column.name] = getattr(row, column.name)
        return query_as_dict
