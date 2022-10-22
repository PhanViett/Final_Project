from application.extensions import ma, db
from application.models.chung_chi_hanh_nghe import ChungChiHanhNghe
from application.schemas.danhmuc_pham_vi_hoat_dong_chuyen_mon import PhamViHoatDongChuyenMonSchema
from application.schemas.danhmuc_vi_tri_hanh_nghe import ViTriHanhNgheSchema
from marshmallow import fields


class ChungChiHanhNgheSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    pham_vi_chuyen_mon = ma.Nested(PhamViHoatDongChuyenMonSchema, many=True)
    vi_tri_hanh_nghe = ma.Nested(ViTriHanhNgheSchema, many=True)
    van_bang_chuyen_mon = fields.String(attribute="van_bang_chuyen_mon.ten")

    class Meta:
        model = ChungChiHanhNghe
        include_fk = True
        include_relationship = True
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at", "deleted", "created_by", "updated_by")


class ChungChiHanhNgheDisplaySchema(ma.SQLAlchemySchema):
    id = ma.auto_field(dump_only=True)
    ho_ten = fields.String(dump_only=True)
    ngay_sinh = fields.Integer(dump_only=True)
    gioi_tinh = fields.String(dump_only=True)
    thoi_gian_lien_ket = fields.Integer(dump_only=True)
    trang_thai = fields.String(dump_only=True)

    class Meta:
        model = ChungChiHanhNghe
        sqla_session = db.session


class ChungChiHanhNgheChuyenMonSchema(ma.SQLAlchemySchema):
    id = ma.auto_field(dump_only=True)
    ho_ten = fields.String(attribute="nhan_vien.ho_ten", dump_only=True)
    ngay_sinh = fields.Integer(attribute="nhan_vien.ngay_sinh", dump_only=True)
    gioi_tinh = fields.String(attribute="gioi_tinh", dump_only=True)
    email = fields.String(attribute="nhan_vien.email", dump_only=True)
    dien_thoai = fields.String(attribute="nhan_vien.dien_thoai", dump_only=True)
    cmnd = fields.String(attribute="nhan_vien.ma_cong_dan", dump_only=True)
    ngay_cap_cmnd = fields.Integer(attribute="nhan_vien.ngay_cap", dump_only=True)
    noi_cap_cmnd = fields.String(attribute="nhan_vien.noi_cap", dump_only=True)

    thoi_gian_lien_ket = fields.Integer(dump_only=True)
    co_quan_cap = fields.String(dump_only=True)
    so_giay_phep = fields.String(dump_only=True)
    ngay_hieu_luc = fields.Integer(dump_only=True)

    class Meta:
        model = ChungChiHanhNghe
        sqla_session = db.session


class CCHNDaCapDisplay(ma.SQLAlchemySchema):
    id = ma.auto_field(dump_only=True)
    ho_ten = fields.String(attribute="nhan_vien.ho_ten", dump_only=True)
    cmnd = fields.String(attribute="nhan_vien.ma_cong_dan", dump_only=True)
    ngay_cap = fields.Integer(dump_only=True)
    co_quan_cap = fields.String(dump_only=True)
    so_giay_phep = fields.String(dump_only=True)

    class Meta:
        model = ChungChiHanhNghe
        sqla_session = db.session


class CCHNInfoSchema(ma.SQLAlchemySchema):
    id = ma.auto_field(dump_only=True)
    so_giay_phep = ma.auto_field()
    ngay_cap = ma.auto_field()
    ngay_hieu_luc = ma.auto_field()
    ngay_het_han = fields.Integer(dump_default=None, allow_none=True)
    so_quyet_dinh = ma.auto_field()
    ngay_quyet_dinh = ma.auto_field()
    van_bang_chuyen_mon_id = ma.auto_field()
    van_bang_chuyen_mon = fields.String(attribute="van_bang_chuyen_mon.ten",  dump_only=True)
    noi_cap = ma.auto_field()
    hinh_thuc_thi = ma.auto_field()
    noi_cong_tac = ma.auto_field()
    dia_chi_cong_tac = ma.auto_field()

    class Meta:
        model = ChungChiHanhNghe
        sqla_session = db.session
