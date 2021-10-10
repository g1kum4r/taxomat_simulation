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
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.bank import bp as bank_ap
    app.register_blueprint(bank_ap)

    from app.citizen import bp as citizen_bp
    app.register_blueprint(citizen_bp)

    from app.dasboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.excise import bp as excise_bp
    app.register_blueprint(excise_bp)

    from app.electricity_provider_companies import bp as epc_bp
    app.register_blueprint(epc_bp)

    from app.fuel_stations import bp as fuel_stations_bp
    app.register_blueprint(fuel_stations_bp)

    from app.sui_gas_provider_companies import bp as sgpc_bp
    app.register_blueprint(sgpc_bp)

    from app.profile import bp as profile_bp
    app.register_blueprint(profile_bp)


    return app
