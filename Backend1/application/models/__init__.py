from flask_bcrypt import Bcrypt
#src/models/__init__.py

from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext


# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


