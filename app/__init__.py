from flask import Flask, url_for
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


mongo = PyMongo()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    from config import Config
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.__init__(app)
    mongo.__init__(app)
    login_manager.__init__(app)

    from app.auth import bp as authBp
    app.register_blueprint(authBp)
    from app.dasboard import bp as dashboardBp
    app.register_blueprint(dashboardBp)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    return app
