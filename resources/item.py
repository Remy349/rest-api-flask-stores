from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_jwt_extended import get_jwt, jwt_required
from db import db

from models import ItemModel

bp = Blueprint("items", __name__, description="Operations on items")


@bp.route("/item/<string:item_id>")
class Item(MethodView):
    @jwt_required()
    @bp.response(200, ItemSchema)
    def get(self, item_id):
        item = db.get_or_404(ItemModel, item_id)
        return item

    @jwt_required()
    @bp.response(204)
    def delete(self, item_id):
        jwt = get_jwt()

        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        item = db.get_or_404(ItemModel, item_id)

        db.session.delete(item)
        db.session.commit()

        return {"message": "Item deleted."}

    @bp.arguments(ItemUpdateSchema)
    @bp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = db.get_or_404(ItemModel, item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@bp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @bp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)
    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An item with that name already exists.")
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return item
