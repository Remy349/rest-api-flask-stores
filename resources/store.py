from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db

from models import StoreModel

bp = Blueprint("stores", __name__, description="Operations on stores")


@bp.route("/store/<string:store_id>")
class Store(MethodView):
    @bp.response(200, StoreSchema)
    def get(self, store_id):
        store = db.get_or_404(StoreModel, store_id)
        return store

    @bp.response(204)
    def delete(self, store_id):
        store = db.get_or_404(StoreModel, store_id)

        db.session.delete(store)
        db.session.commit()

        return {"message": "Store deleted."}


@bp.route("/store")
class StoreList(MethodView):
    @bp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @bp.arguments(StoreSchema)
    @bp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return store
