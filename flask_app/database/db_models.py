# flask_app/db_models.py
import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return f'<User {self.login}>'


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f'<Roles {self.name}>'


class UsersRoles(Base):
    """Таблица связи между пользователями и ролями"""
    __tablename__ = 'users_roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id))
    role_id = Column(UUID(as_uuid=True), ForeignKey(Roles.id))


class History(Base):
    __tablename__ = 'history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id))
    user_agent = Column(String, nullable=False)
    auth_date = Column(DateTime, nullable=False)
