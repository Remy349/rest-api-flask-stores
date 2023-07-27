import sqlalchemy as sa
from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(80), unique=False, nullable=False)

    store_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("stores.id"),
        unique=False,
        nullable=False,
    )

    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship(
        "ItemModel",
        back_populates="tags",
        secondary="items_tags",
    )
