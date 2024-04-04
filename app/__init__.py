from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config, SECRET_KEY
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)
app.secret_key = SECRET_KEY
app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)


app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='muthonimuriuki22@gmail.com',  # Your Gmail address
    MAIL_PASSWORD='',  # Leave this blank
)


from .views import auth, properties, units, work_orders, repairs,email

app.register_blueprint(auth.bp)
app.register_blueprint(properties.bp)
app.register_blueprint(units.bp)
app.register_blueprint(work_orders.bp)
app.register_blueprint(repairs.bp)
