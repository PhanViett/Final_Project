from datetime import datetime
from typing import List
from marshmallow import fields
from application.extensions import ma, db
from application.models import GiayPhepKinhDoanh, LoaiHinhKinhDoanh
from application.models.co_so_kinh_doanh import CoSoKinhDoanh


class GiayPhepKinhDoanhSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)

    class Meta:
        model = GiayPhepKinhDoanh
        include_fk = True
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "created_by", "updated_at", "deleted_at")


class GiayPhepKinhDoanhLKDisplaySchema(ma.SQLAlchemySchema):
    id = ma.auto_field(dump_only=True)
    ten_co_so = fields.String(attribute="ten_coso", dump_only=True)
    dia_diem_kinh_doanh = fields.String(attribute="diachi_kinh_doanh", dump_only=True)
    so_giay_phep = ma.auto_field(dump_only=True)
    ngay_cap = ma.auto_field(dump_only=True)
    ngay_het_han = ma.auto_field(dump_only=True)
    thoi_gian_yeu_cau_lien_ket = fields.Integer(attribute="thoigian_yeucau_lienket", dump_only=True)

    class Meta:
        model = GiayPhepKinhDoanh
        sqla_session = db.session
        load_instance = True


class GiayPhepKinhDoanhInfoSchema(ma.SQLAlchemySchema):
    id = ma.auto_field(dump_only=True)
    ten_co_so = fields.String(attribute="co_so_kinh_doanh.ten_coso", dump_only=True)
    dia_chi_co_so = fields.String(attribute="co_so_kinh_doanh.diachi_coso", dump_only=True)
    dia_diem_kinh_doanh = fields.String(attribute="co_so_kinh_doanh.diachi_kinh_doanh", dump_only=True)
    co_quan_cap = ma.auto_field(dump_only=True)
    so_giay_phep = ma.auto_field(dump_only=True)
    ngay_hieu_luc = ma.auto_field(dump_only=True)
    ngay_het_han = ma.auto_field(dump_only=True)
    trang_thai_ho_so = ma.auto_field(dump_only=True)
    nguoi_chiu_tncm = fields.String(attribute="co_so_kinh_doanh.duoc_si_ctncm.duoc_si.ho_ten",
                                    allow_none=True, dump_default=None, dump_only=True)

    class Meta:
        model = GiayPhepKinhDoanh
        sqla_session = db.session
        load_instance = True


class GiayPhepKinhDoanhDisplaySchema(ma.SQLAlchemySchema):
    id = ma.auto_field(dump_only=True)
    ten_co_so = fields.String(attribute="ten_coso", dump_only=True)
    dia_diem_kinh_doanh = fields.Method("get_dia_chi_kinh_doanh")
    so_gcn = fields.String(attribute="so_gcn", allow_none=True, dump_default=None, dump_only=True)
    co_quan_cap = ma.auto_field(dump_only=True)
    so_giay_phep = ma.auto_field(dump_only=True)
    ngay_het_han = ma.auto_field(dump_only=True)
    nguoi_ctncm = fields.String(attribute="nguoi_ctncm",
                                allow_none=True, dump_default=None, dump_only=True)
    tinh_trang = fields.Method("get_tinh_trang")

    class Meta:
        model = GiayPhepKinhDoanh
        sqla_session = db.session
        load_instance = True

    def get_tinh_trang(self, obj):
        if obj and obj.ngay_het_han:
            x = int(datetime.now().timestamp())
            if x > obj.ngay_het_han:
                return False
        return True

    def get_loai_hinh_lien_ket(self, obj):
        if obj and len(obj.loai_hinh_kinh_doanh) > 0:
            danh_sach_lhkd: List[LoaiHinhKinhDoanh] = obj.loai_hinh_kinh_doanh
            lhkd = ", ".join([x.ten for x in danh_sach_lhkd])
            return lhkd
        return None

    def get_dia_chi_kinh_doanh(self, obj):
        dia_chi_list = []
        if obj and obj.diachi_kinh_doanh:
            dia_chi_list.append(obj.diachi_kinh_doanh)
        dia_chi_list.extend([
            obj.xa_phuong,
            obj.quan_huyen
        ])
        return ", ".join(filter(None, dia_chi_list))
