from datetime import datetime
import uuid
import time
from math import floor
from sqlalchemy.dialects.postgresql import UUID
from application.extensions import db

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, String, Integer, BigInteger,
    DateTime, Date, Boolean,
    event, func
)


def default_uuid():
    return str(uuid.uuid4())


def model_oncreate_listener(mapper, connection, instance):
    instance.created_at = floor(time.time())
    instance.updated_at = floor(time.time())


def model_onupdate_listener(mapper, connection, instance):
    instance.created_at = instance.created_at
    instance.updated_at = floor(time.time())
    if instance.deleted is True:
        instance.deleted_at = floor(time.time())


# CommonModel
# a common model using to add all below attributes into model class
# using CommonModel as argument of Model Class
class CommonModel(db.Model):
    __abstract__ = True
#     id = db.Column(UUID(as_uuid=True), default=default_uuid)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=True)
    created_by = db.Column(db.String, nullable=True)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=True)
    updated_by = db.Column(db.String, nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String, nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)


# event.listen(CommonModel, 'before_insert', model_oncreate_listener, propagate=True)
# event.listen(CommonModel, 'before_update', model_onupdate_listener, propagate=True)
