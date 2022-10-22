from application.extensions import ma, db
from application.models.chung_chi_hanh_nghe import ChungChiHanhNghe
from application.models.co_so_kinh_doanh import CoSoKinhDoanh
from application.schemas.danhmuc_loai_hình_kinh_doanh import LoaiHinhKinhDoanhSchema
from application.schemas.danhmuc_pham_vi_hoat_dong_kinh_doanh import PhamVihoatDongKinhDoanhSchema
from marshmallow import fields
from flask_jwt_extended import current_user
from application.schemas.vai_tro import VaiTroSchema


class CoSoKinhDoanhSchema(ma.SQLAlchemyAutoSchema):
    assigned_role = ma.Nested(VaiTroSchema, many=True)
    id = ma.auto_field(dump_only=True)
    taikhoan_id = ma.auto_field()
    ten_kinhdoanh_khongdau = ma.auto_field(dump_only=True)
    last_login = fields.DateTime(format="%H:%M:%S %d/%m/%Y",
                                 attribute="tai_khoan.last_login_at", dump_only=True, default=None)
    ten_truc_thuoc_khong_dau = ma.auto_field(dump_only=True)
    ten_coso_khongdau = ma.auto_field(dump_only=True)
    loai_hinh_kinh_doanh = ma.Nested(LoaiHinhKinhDoanhSchema, many=True)
    pham_vi_kinh_doanh = ma.Nested(PhamVihoatDongKinhDoanhSchema, many=True)
    # van_bang_chuyen_mon = fields.String(attribute="van_bang_chuyen_mon.ten")

    class Meta:
        model = CoSoKinhDoanh
        include_fk = True
        include_relationship = True
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at", "deleted", "created_by", "updated_by")
