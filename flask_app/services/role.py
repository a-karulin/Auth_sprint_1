import sqlalchemy.orm
from flask import abort
from sqlalchemy.exc import NoResultFound

from database.db import engine
from database.db_models import Roles, UsersRoles
from database.session_decorator import get_session


class RoleService:
    def __init__(self):
        self.engine = engine

    @get_session()
    def apply_user_role(
            self,
            user_id: str,
            role_id: str,
            session: sqlalchemy.orm.Session = None
    ):
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
    ):
        try:
            role = session.query(UsersRoles).filter(
                UsersRoles.user_id == user_id,
                UsersRoles.role_id == role_id,
            ).one()
            session.delete(role)
            session.commit()
        except NoResultFound:
            abort(409)

    @get_session()
    def get_role(
            self,
            role_name,
            session: sqlalchemy.orm.Session = None
    ):
        try:
            role = session.query(Roles).filter(role=role_name).one()
            return role
        except NoResultFound:
            abort(404)
