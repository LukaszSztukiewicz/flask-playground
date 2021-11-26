from flask import Flask
import os
from src.auth import auth
from src.database import db, Bookmark
from src.bookmarks import bookmarks
from flask_jwt_extended import JWTManager
from src.database import User
from src.database import Bookmark
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Bookmark, db.session))

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            FLASK_ADMIN_SWATCH='cerulean'
            )
    else:
        app.config.from_mapping(test_config)
    
    db.app = app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    return app

#1:26:23