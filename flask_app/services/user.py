import sqlalchemy.orm
from flask import Response
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
            user = session.query(User).filter(User.login == login).one()
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
            return Response(
                "{'result':'user with this login already exists'}",
                status=400,
                mimetype='application/json',
            )
