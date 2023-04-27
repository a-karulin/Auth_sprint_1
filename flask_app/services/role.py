from http import HTTPStatus

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

    @get_session()
    def create_role(
            self,
            role_name,
            session: sqlalchemy.orm.Session = None
    ):
        if session.query(Roles).filter(Roles.role == role_name).first():
            return {"msg": "Role exists in database"}, HTTPStatus.CONFLICT
        session.add(Roles(role=role_name))
        session.commit()
        return {"msg": "Created new role"}, HTTPStatus.CREATED

    @get_session()
    def update_role(
            self,
            role_id,
            role_name,
            session: sqlalchemy.orm.Session = None
    ):
        if session.query(Roles).filter(Roles.id == role_id).first():
            return {"msg": "Role doesn't exist in database"}, HTTPStatus.NOT_FOUND
        if session.query(Roles).filter(Roles.role == role_name).first():
            return {"msg": "Role with this name already exist"}, HTTPStatus.CONFLICT
        session.query(Roles).filter_by(id=role_id).update({"name": role_name})
        session.commit()
        return {"msg": "Updated role"}, HTTPStatus.CREATED

    @get_session()
    def delete_role(
            self,
            role_id,
            session: sqlalchemy.orm.Session = None
    ):
        if not session.query(Roles).filter(Roles.id == role_id).first():
            return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND
        session.query(Roles).filter_by(id=role_id).delete()
        session.commit()
        return {"msg": "Deleted role"}, HTTPStatus.OK
