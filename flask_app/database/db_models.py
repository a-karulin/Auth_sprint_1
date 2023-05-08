# flask_app/db_models.py
import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role = Column(String, unique=True, nullable=False)


class UsersRoles(Base):
    """Таблица связи между пользователями и ролями"""
    __tablename__ = 'users_roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    role_id = Column(UUID(as_uuid=True), nullable=False)


class History(Base):
    __tablename__ = 'history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete='CASCADE'))
    user_agent = Column(String, nullable=False)
    auth_date = Column(DateTime, nullable=False)


class OauthUsers(Base):
    __tablename__ = 'oauth_users'
    __table_args__ = UniqueConstraint('oauth_id', 'oauth_email', name='oauth_unique'),

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    oauth_id = Column(Text, nullable=False)
    oauth_email = Column(Text, nullable=False)
