import sqlalchemy.orm
from flask import abort
from sqlalchemy.exc import NoResultFound

from database.db import engine
from database.db_models import Roles
from database.session_decorator import get_session


class RoleService:
    def __init__(self):
        self.engine = engine

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

