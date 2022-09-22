import re
from typing import cast
import uuid
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.ext.hybrid import hybrid_property
import datetime
from sqlalchemy.sql.expression import true
from sqlalchemy.orm import validates
from application.extensions import db, pwd_context
from flask_jwt_extended import current_user
from sqlalchemy.dialects import postgresql
from sqlalchemy import event, func, Index


class NhanVien(db.Model):
    """Basic nhan_vien model"""
    __tablename__ = "nhan_vien"

    # PROPERTIES
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tai_khoan_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tai_khoan.id"), nullable=True)
    email = db.Column(db.String(80), nullable=True)
    ho = db.Column(db.String(80), nullable=True)
    ten = db.Column(db.String(80), nullable=True)
    dia_chi = db.Column(db.String, nullable=True)
    so_dien_thoai = db.Column(db.String(12), nullable=True)
    active = db.Column(db.Boolean, default=True)
    is_super_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)
    vai_tro_id = db.Column(UUID(as_uuid=True), db.ForeignKey("vai_tro.id"), nullable=True)
    # region RELATIONSHIPS
    assigned_role = db.relationship("VaiTro", backref="nhan_vien", lazy="joined")
    assigned_account = db.relationship("TaiKhoan", backref="nhan_vien", lazy="joined")
    # endregion

    def __repr__(self):
        return "<NhanVien %s>" % self.ten

    def __init__(self, tai_khoan_id=None, email=None, active=None, vai_tro_id=None,
                 ho=None, ten=None, dia_chi=None, so_dien_thoai=None, is_super_admin=False):
        self.id = uuid.uuid4()
        self.tai_khoan_id = tai_khoan_id
        self.email = email
        self.ho = ho
        self.ten = ten
        self.dia_chi = dia_chi
        self.so_dien_thoai = so_dien_thoai
        self.is_super_admin = is_super_admin
        self.active = active
        self.vai_tro_id = vai_tro_id

    def __str__(self):
        return "ID=%d, Email=%s, last_name=%s, first_name=%s, address=%s, phone=%s" % \
               (self.id, self.email, self.ho, self.ten, self.dia_chi,
                self.so_dien_thoai)

    def create_tsvector(*args):
        exp = args[0]
        for e in args[1:]:
            exp += ' ' + e
        return func.to_tsvector('english', exp)

    __ts_vector__ = create_tsvector(
        cast(func.coalesce(ten, ''), postgresql.TEXT)
    )

    __table_args__ = (
        Index(
            'idx_user_fts',
            __ts_vector__,
            postgresql_using='gin'
        ),
    )

# TRIGGERS


@event.listens_for(NhanVien, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(NhanVien, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()
