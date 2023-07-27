import os
import models

from flask import Flask
from flask_smorest import Api
from db import db
from flask_jwt_extended import JWTManager

from resources.item import bp as item_bp
from resources.store import bp as store_bp
from resources.tag import bp as tag_bp
from resources.user import bp as user_bp

jwt = JWTManager()


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "e9d7b1069769c8c53af3238193493ca1"

    db.init_app(app)
    jwt.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(item_bp)
    api.register_blueprint(store_bp)
    api.register_blueprint(tag_bp)
    api.register_blueprint(user_bp)

    return app
