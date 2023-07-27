from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models.item import ItemModel
from schemas import TagAndItemSchema, TagSchema

from models import TagModel, StoreModel

bp = Blueprint("tags", __name__, description="Operations on tags")


@bp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @bp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = db.get_or_404(StoreModel, store_id)
        return store.tags.all()

    @bp.arguments(TagSchema)
    @bp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(
            TagModel.store_id == store_id, TagModel.name == tag_data["name"]
        ).first():
            abort(
                400,
                message="A tag with that name already exists in that store.",
            )

        tag = TagModel(**tag_data)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@bp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @bp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = db.get_or_404(ItemModel, item_id)
        tag = db.get_or_404(TagModel, tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

    @bp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = db.get_or_404(ItemModel, item_id)
        tag = db.get_or_404(TagModel, tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return {"message": "Item removed from tag", "item": item, "tag": tag}


@bp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @bp.response(200, TagSchema)
    def get(self, tag_id):
        tag = db.get_or_404(TagModel, tag_id)
        return tag

    @bp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    def delete(self, tag_id):
        tag = db.get_or_404(TagModel, tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}

        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",
        )
