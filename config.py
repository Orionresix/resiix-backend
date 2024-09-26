import os


GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
AUTHORIZATION_URL = os.environ.get("auth_uri", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
SECRET_KEY = os.environ.get("secret_key", None)
UPLOAD_FOLDER = 'resiix/images/'


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USERNAME = os.environ.get('Usernameprod')
    AFRICA_TALKING_KEY = os.environ.get('AFRICA_TALKING_api_key_prod')
