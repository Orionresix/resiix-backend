from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY, Config
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from .views.auth import login_manager, auth_bp


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_blueprints(app)
    login_manager.init_app(app)
    app.secret_key = SECRET_KEY
    app.config['JWT_SECRET_KEY'] = SECRET_KEY
    
    mail = Mail(app)
    jwt = JWTManager(app)
    db = SQLAlchemy(app)
    CORS(app)
    return app


def register_blueprints(app):
    from .views import auth, properties, units, work_orders, repairs, technicians
    app.register_blueprint(auth_bp)
    app.register_blueprint(properties.bp)
    app.register_blueprint(units.bp)
    app.register_blueprint(work_orders.bp)
    app.register_blueprint(repairs.bp)
    app.register_blueprint(technicians.bp)
