from application.extensions import ma, db
from application.models.chung_chi_hanh_nghe import ChungChiHanhNghe
from application.models.chung_nhan_thuc_hanh_co_so import ChungNhanCoSo
from application.models.co_so_kinh_doanh import CoSoKinhDoanh
from application.models.duoc_si_co_so import DuocSiCoSo
from application.schemas.danhmuc_loai_hình_kinh_doanh import LoaiHinhKinhDoanhSchema
from application.schemas.danhmuc_pham_vi_hoat_dong_kinh_doanh import PhamVihoatDongKinhDoanhSchema
from marshmallow import fields


class DuocSiCoSoSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    duoc_si_id = ma.auto_field()
    co_so_kinh_doanh_id = ma.auto_field()

    class Meta:
        model = DuocSiCoSo
        include_fk = True
        # include_relationship = True
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at", "deleted", "created_by", "updated_by")


class DuocSiCoSoDisplaySchema(ma.SQLAlchemySchema):
    id = ma.auto_field(dump_only=True)
    ho_ten = fields.String(attribute="ho_ten", dump_only=True)
    ngay_sinh = fields.String(attribute="ngay_sinhh", dump_only=True)
    dien_thoai = fields.String(attribute="dien_thoai", dump_only=True)
    chung_chi_hanh_nghe = fields.String(attribute="so_giay_phep",
                                        allow_empty=True, dump_default=None, dump_only=True)
    hieu_luc_den = fields.String(attribute="hieu_luc_den",
                                 allow_empty=True, dump_default=None, dump_only=True)
    ngay_kiem_tra = fields.String(attribute="ngay_kiem_tra",
                                  allow_empty=True, dump_default=None, dump_only=True)
    vai_tro = ma.auto_field(dump_only=True)

    class Meta:
        model = DuocSiCoSo
        include_fk = True
        sqla_session = db.session
        load_instance = True
