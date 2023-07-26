import sqlalchemy as sa
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(80), unique=True, nullable=False)
    price = sa.Column(sa.Float(precision=2), unique=False, nullable=False)

    store_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("stores.id"),
        unique=False,
        nullable=False,
    )

    store = db.relationship("StoreModel", back_populates="items")
