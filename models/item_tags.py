import sqlalchemy as sa
from db import db


class ItemsTags(db.Model):
    __tablename__ = "items_tags"

    id = sa.Column(sa.Integer, primary_key=True)
    item_id = sa.Column(sa.Integer, sa.ForeignKey("items.id"))
    tag_id = sa.Column(sa.Integer, sa.ForeignKey("tags.id"))
