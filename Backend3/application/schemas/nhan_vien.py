from enum import unique
from application.models import Users
from application.extensions import ma, db
from marshmallow import fields


class NhanVienSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    email = fields.Email()
    vai_tro_id = ma.auto_field()
    tai_khoan_id = ma.auto_field(load_only=True)

    class Meta:
        model = Users
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")


class NguoiDungDisplaySchema(ma.SQLAlchemySchema):
    id = fields.String(dump_only=True)
    ho_ten = fields.String(dump_only=True)
    active = fields.Boolean(dump_only=True)
    tai_khoan = fields.String(attribute="tai_khoan.tai_khoan", allow_none=True, dump_default=None, dump_only=True)
    email = fields.String(dump_only=True)
    ho = fields.String(dump_only=True)
    ten = fields.String(dump_only=True)
    ngay_sinh = fields.String(dump_only=True)
    gioi_tinh = fields.String(dump_only=True)
    gioithieu = fields.String(dump_only=True)
    avatar_url = fields.String(dump_only=True)
    dien_thoai = fields.String(dump_only=True)

    class Meta:
        model = Users
        sqla_session = db.session
        load_instance = True


# ONLY FOR SHOW
class NhanVienWithRoleSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    mat_khau = ma.String(load_only=True, required=True)
    email = fields.Email()
    vai_tro_id = ma.String(load_only=True)

    class Meta:
        model = Users
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")


class NhanVienForSwaggerSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    email = fields.Email()
    vai_tro_id = ma.auto_field()
    tai_khoan = fields.String()
    mat_khau = fields.String()

    class Meta:
        model = Users
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at", )


class NhanVienWithTaiKhoanSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    email = fields.Email()
    vai_tro_id = ma.auto_field()
    tai_khoan_id = ma.auto_field(load_only=True)
    ten_tai_khoan = fields.String(attribute="assigned_account.tai_khoan", dump_only=True)

    class Meta:
        model = Users
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")
