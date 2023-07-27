from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import UserSchema
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token

from models import UserModel

bp = Blueprint("users", __name__, description="Operations on users")


@bp.route("/register")
class UserRegister(MethodView):
    @bp.arguments(UserSchema)
    @bp.response(201)
    def post(self, user_data):
        if UserModel.query.filter(
            UserModel.username == user_data["username"],
        ).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            password=generate_password_hash(user_data["password"]),
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}


@bp.route("/user/<int:user_id>")
class User(MethodView):
    @bp.response(200, UserSchema)
    def get(self, user_id):
        user = db.get_or_404(UserModel, user_id)
        return user

    @bp.response(204)
    def delete(self, user_id):
        user = db.get_or_404(UserModel, user_id)

        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted."}


@bp.route("/login")
class UserLogin(MethodView):
    @bp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and check_password_hash(user.password, user_data["password"]):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")
