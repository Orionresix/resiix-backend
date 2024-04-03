from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config, SECRET_KEY
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)

from .views import auth, properties, units, work_orders, repairs

app.register_blueprint(auth.bp)
app.register_blueprint(properties.bp)
app.register_blueprint(units.bp)
app.register_blueprint(work_orders.bp)
app.register_blueprint(repairs.bp)
