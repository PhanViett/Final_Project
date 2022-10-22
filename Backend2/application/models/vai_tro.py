from datetime import datetime
import uuid
from flask_jwt_extended.view_decorators import jwt_required, verify_jwt_in_request
from sqlalchemy import event
from flask import json
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.sql.functions import user
from application.extensions import db
from flask_jwt_extended import current_user

from application.models.user import User
from application.utils.helper.string_processing_helper import clean_string


class VaiTro(db.Model):
    __tablename__ = "vai_tro"

    # PROPERTIES
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ten = db.Column(db.String(80), unique=True, nullable=False)
    ten_en = db.Column(db.String, nullable=True)
    created_by = db.Column(UUID(as_uuid=True), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=True)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    def __init__(self,  ten: str = None) -> None:
        self.ten = ten
        self.ten_en = clean_string(ten)

# TRIGGERS


@event.listens_for(VaiTro, "before_insert")
def on_insert_trigger(mapper, connection, target):
    table = VaiTro.__table__
    verify_jwt_in_request()
    user: User = current_user
    target.created_by = user.id
    target.created_at = datetime.now()
    target.updated_at = datetime.now()


@event.listens_for(VaiTro, "before_update")
def on_update_trigger(mapper, connection, target):
    table = VaiTro.__table__
    target.updated_at = datetime.now()
