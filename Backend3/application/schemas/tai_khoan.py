from marshmallow import fields
from application.extensions import ma, db
from application.models.tai_khoan import TaiKhoan


class TaiKhoanSchema(ma.SQLAlchemySchema):
    id = fields.String(dump_only=True)
    tai_khoan = fields.String(dump_only=True)
    last_login_at = fields.String(dump_only=True)
    mat_khau = fields.String(dump_only=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)

    class Meta:
        model = TaiKhoan
        sqla_session = db.session
