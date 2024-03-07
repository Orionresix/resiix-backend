from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Import routes after creating the Flask app to avoid circular imports
from app.routes import *

if __name__ == '__main__':
    app.run(debug=True)