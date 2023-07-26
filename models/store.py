import sqlalchemy as sa
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(80), unique=True, nullable=False)

    items = db.relationship(
        "ItemModel",
        back_populates="store",
        lazy="dynamic",
        cascade="all, delete",
    )
