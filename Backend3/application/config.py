"""Default configuration

Use env var to override
"""
from datetime import timedelta
import os


ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)
# CONFIG MINIO
MINIO_URL = os.getenv("MINIO_URL")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_DECODE_RESPONSES = os.getenv("REDIS_DECODE_RESPONSES")

DEFAULT_ADMIN_DON_VI_ID = os.getenv("DEFAULT_ADMIN_DON_VI_ID")
DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID")