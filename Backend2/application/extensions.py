"""Extensions registry
All extensions here are used as singletons and
initialized in application factory
"""
import hashlib
import os
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import redis
from application.commons.apispec import APISpecExt
from firebase_admin import credentials
import firebase_admin
# from celery import Celery

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
apispec = APISpecExt()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

