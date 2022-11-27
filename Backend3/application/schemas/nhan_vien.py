from marshmallow import fields
from application.models import Users
from application.extensions import ma, db
from application.schemas.vai_tro import VaiTroSchema


class NhanVienSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    email = fields.Email()
    vai_tro_id = ma.auto_field()
    tai_khoan_id = ma.auto_field(load_only=True)
    assigned_role = ma.Nested(VaiTroSchema, many=True)
    tinh_thanh_hien_nay_id = ma.auto_field()
    tinh_thanh_thuong_tru_id = ma.auto_field()
    quan_huyen_hien_nay_id = ma.auto_field()
    quan_huyen_thuong_tru_id = ma.auto_field()
    xa_phuong_hien_nay_id = ma.auto_field()
    xa_phuong_thuong_tru_id = ma.auto_field()
    
    class Meta:
        model = Users
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")

class NhanVienUpdateSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    avatar_url = ma.auto_field(load_only=True)
    ho = ma.auto_field()
    ten = ma.auto_field()
    ngay_sinh = ma.auto_field()
    gioi_tinh = ma.auto_field()
    ma_cong_dan = ma.auto_field()
    ngay_cap = ma.auto_field()
    noi_cap = ma.auto_field()
    dien_thoai = ma.auto_field()
    email = ma.auto_field()
    tinh_thanh_hien_nay_id = ma.auto_field()
    quan_huyen_hien_nay_id = ma.auto_field()
    xa_phuong_hien_nay_id = ma.auto_field()
    so_nha_hien_nay = ma.auto_field()
    tinh_thanh_thuong_tru_id = ma.auto_field()
    quan_huyen_thuong_tru_id = ma.auto_field()
    xa_phuong_thuong_tru_id = ma.auto_field()
    so_nha_thuong_tru = ma.auto_field()


    class Meta:
        model = Users
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")

class NhanVienRecordSchema(ma.SQLAlchemySchema):
    ho_ten = ma.auto_field()
    ngay_sinh = ma.auto_field()
    gioi_tinh = ma.auto_field()
    height = ma.auto_field()
    weight = ma.auto_field()
    chol = ma.auto_field()
    gluc = ma.auto_field()
    smoke = ma.auto_field()
    alco = ma.auto_field()
    active = ma.auto_field()

    class Meta:
        model = Users
        sqla_session = db.session
        load_instance = True
            # exclude = ("created_at", "updated_at", "deleted_at")

class NguoiDungDisplaySchema(ma.SQLAlchemySchema):
    id = fields.String(dump_only=True)
    ho_ten = fields.String(dump_only=True)
    active = fields.Boolean(dump_only=True)
    tai_khoan = fields.String(attribute="tai_khoan.tai_khoan")
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
