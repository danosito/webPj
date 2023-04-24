import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Works(SqlAlchemyBase):
    __tablename__ = 'works'

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)