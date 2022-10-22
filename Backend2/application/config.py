"""Default configuration

Use env var to override
"""
from datetime import timedelta
import os

FLASK_BUILD_VERSION = os.getenv("FLASK_BUILD_VERSION")
FLASK_BUILD_DATE = os.getenv("FLASK_BUILD_DATE")
TZ = os.getenv("TZ")

FLASK_DEBUG = os.getenv("FLASK_DEBUG", False) == "True"
DEBUG = FLASK_DEBUG
SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)

DEFAULT_ADMIN_DON_VI_ID = os.getenv("DEFAULT_ADMIN_DON_VI_ID")
DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID")
