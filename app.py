import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.ext.session import Session



SESSION_TYPE = 'memcache'

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
sess = Session()



if __name__ == '__main__':
    sess.init_app(app)
    app.run(debug=True)
