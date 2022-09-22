from enum import unique
import re
from flask import json
from marshmallow_sqlalchemy.schema import auto_field
from application.models import NhanVien
from application.extensions import ma, db

from marshmallow import ValidationError, fields, validates

from application.utils.validate.uuid_validator import is_valid_uuid


class NhanVienSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    is_super_admin = ma.auto_field(load_only=True)
    email = fields.Email()
    vai_tro_id = ma.auto_field()
    tai_khoan_id = ma.auto_field(load_only=True)
    last_login = fields.DateTime(attribute="assigned_account.last_login_at", dump_only=True, default=None)

    class Meta:
        model = NhanVien
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")

    @validates('so_dien_thoai')
    def validate_phone_number(self, phone_number):
        if not phone_number:
            return None
        only_digits_pattern = re.compile("^[ 0-9]+$")
        if not only_digits_pattern.fullmatch(phone_number) != None:
            raise ValidationError("Số điện thoại không phù hợp")

# ONLY FOR SHOW
class NhanVienWithRoleSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    mat_khau = ma.String(load_only=True, required=True)
    email = fields.Email()
    vai_tro_id = ma.String(load_only=True)

    class Meta:
        model = NhanVien
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")


class NhanVienForSwaggerSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    is_super_admin = ma.auto_field(load_only=True)
    email = fields.Email()
    vai_tro_id = ma.auto_field()
    tai_khoan = fields.String()
    mat_khau = fields.String()

    class Meta:
        model = NhanVien
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at", )


class NhanVienWithTaiKhoanSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    is_super_admin = ma.auto_field(load_only=True)
    email = fields.Email()
    vai_tro_id = ma.auto_field()
    tai_khoan_id = ma.auto_field(load_only=True)
    ten_tai_khoan = fields.String(attribute="assigned_account.tai_khoan", dump_only=True)

    class Meta:
        model = NhanVien
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")
