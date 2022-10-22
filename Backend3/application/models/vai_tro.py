import datetime
import uuid
from flask_jwt_extended.view_decorators import jwt_required, verify_jwt_in_request
from sqlalchemy import event
from flask import json
from flask_seeder.generator import String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.sql.functions import user
from application.extensions import db
from flask_jwt_extended import current_user

from application.models.nhan_vien import Users
from application.utils.helper.string_processing_helper import clean_string


class VaiTro(db.Model):
    __tablename__ = "vai_tro"

    # PROPERTIES
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ten = db.Column(db.String(80), unique=True, nullable=False)
    ten_en = db.Column(db.String, nullable=True)
    created_by = db.Column(UUID(as_uuid=True), nullable=False)
    created_at = db.Column(db.BigInteger, nullable=True)
    updated_at = db.Column(db.BigInteger, nullable=True)
    deleted_at = db.Column(db.BigInteger, nullable=True)

    def __repr__(self) -> str:
        return f"<Role {self.name}>"

    def __init__(self,  ten: str = None,
                 vai_tro: str = None) -> None:
        self.ten = ten
        self.vai_tro = vai_tro
        self.ten_en = clean_string(ten)

    def __str__(self) -> String:
        return f"id={self.id}, name={self.ten}, permission={self.vai_tro}, description={self.mo_ta}"

# TRIGGERS


@event.listens_for(VaiTro, "before_insert")
def on_insert_trigger(mapper, connection, target):
    table = VaiTro.__table__
    verify_jwt_in_request()
    user: Users = current_user
    target.created_by = user.id
    target.created_at = get_current_time("int")
    target.updated_at = get_current_time("int")


@event.listens_for(VaiTro, "before_update")
def on_update_trigger(mapper, connection, target):
    table = VaiTro.__table__
    target.updated_at = get_current_time("int")
