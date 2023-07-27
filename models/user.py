import sqlalchemy as sa
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(80), unique=True, nullable=False)
    password = sa.Column(sa.String(80), nullable=False)
