from datetime import datetime
from enum import unique
import json
from application.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from application.commons.commons import CommonModel
from application.extensions import db
from sqlalchemy import event
from flask_jwt_extended import current_user
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from application.utils.helper.generate_so_thu_tu import generate_number
from application.utils.helper.string_processing_helper import clean_string


def generate_ma_ho_so():
    so_thu_tu = generate_number("yeu_cau_dkkd")
    data = "HS" + str(so_thu_tu).zfill(7)
    return data


class YeuCauDangKyKinhDoanh(CommonModel):

    __tablename__ = "yeu_cau_dang_ky_kinh_doanh"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ma_ho_so = db.Column(db.String, nullable=True)
    co_so_kinh_doanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("co_so_kinh_doanh.id"), nullable=True)
    thong_tin_co_so_kinh_doanh = db.Column(MutableDict.as_mutable(JSONB), nullable=True)
    loai_yeu_cau = db.Column(db.String, nullable=True)
    thu_tuc_id = db.Column(UUID(as_uuid=True), db.ForeignKey("danhmuc_thu_tuc.id"), nullable=True)
    ma_thu_tuc_bo_sung = db.Column(UUID(as_uuid=True), db.ForeignKey("danhmuc_thu_tuc.id"), nullable=True)
    ngay_nop_ho_so = db.Column(db.String, nullable=True)
    co_quan_cap = db.Column(db.String, nullable=True)
    ngay_cap = db.Column(db.String, nullable=True)
    ngay_hieu_luc = db.Column(db.String, nullable=True)
    ngay_het_han = db.Column(db.String, nullable=True)
    lan_cap_thu = db.Column(db.String, nullable=True)
    so_chung_chi_moi = db.Column(db.String, nullable=True)
    loai_ma_chung_chi = db.Column(db.String, nullable=True)
    thay_the_chung_chi = db.Column(db.String, nullable=True)
    hoi_dong_id = db.Column(UUID(as_uuid=True), db.ForeignKey("danhmuc_hoi_dong.id"), nullable=True)
    so_quyet_dinh = db.Column(db.String, nullable=True)
    ngay_quyet_dinh = db.Column(db.String, nullable=True)
    loai_ma_chung_chi_gps = db.Column(db.String, nullable=True)
    so_chung_nhan_gps = db.Column(db.String, nullable=True)
    ngay_cap_gps = db.Column(db.String, nullable=True)
    ngay_het_han_gps = db.Column(db.String, nullable=True)
    danh_sach_chung_nhan_gps = db.Column(JSONB, nullable=True)
    danh_sach_chung_nhan_kinh_doanh = db.Column(JSONB, nullable=True)
    danh_sach_nguoi_hanh_nghe = db.Column(JSONB, nullable=True)
    ly_do_cap_lai = db.Column(db.String, nullable=True)
    noi_dung_dieu_chinh = db.Column(db.String, nullable=True)
    noi_dung_tham_xet = db.Column(db.String, nullable=True)
    noi_dung_de_nghi = db.Column(db.String, nullable=True)
    noi_dung_yeu_cau = db.Column(db.String, nullable=True)
    ma_nguoi_cap_nhat = db.Column(db.String, nullable=True)
    ten_nguoi_cap_nhat = db.Column(db.String, nullable=True)
    thoi_gian_cap_nhat = db.Column(db.String, nullable=True)
    ma_nguoi_thu_ly = db.Column(db.String, nullable=True)
    ten_nguoi_thu_ly = db.Column(db.String, nullable=True)
    nguoi_thu_ly = db.Column(db.String, nullable=True)
    y_kien_lanh_dao = db.Column(db.String, nullable=True)
    dinh_kem_don_de_nghi = db.Column(db.String, nullable=True)
    dinh_kem_chung_chi_da_cap = db.Column(db.String, nullable=True)
    dinh_kem_cchnd_thay_doi = db.Column(db.String, nullable=True)
    dinh_kem_cndkkdd_gps = db.Column(db.String, nullable=True)
    dinh_kem_so_do_nhansu = db.Column(db.String, nullable=True)
    dinh_kem_so_do_co_so = db.Column(db.String, nullable=True)
    dinh_kem_trang_thiet_bi = db.Column(db.String, nullable=True)
    dinh_kem_ho_so = db.Column(db.String, nullable=True)
    dinh_kem_kiem_tra_thuc_hanh = db.Column(db.String, nullable=True)
    dinh_kem_chung_nhan_co_so = db.Column(db.String, nullable=True)
    dinh_kem_chung_chi_hanh_nghe = db.Column(db.String, nullable=True)
    dinh_kem_tai_lieu_thuyet_minh = db.Column(db.String, nullable=True)
    dinh_kem_xac_nhan_le_phi = db.Column(db.String, nullable=True)
    dinh_kem_files_khac = db.Column(db.String, nullable=True)
    dinh_kem_chung_nhan_bi_sai = db.Column(db.String, nullable=True)
    dinh_kem_ban_sao_cchnd = db.Column(db.String, nullable=True)
    dinh_kem_chung_nhan_dang_ky_doanh_nghiep = db.Column(db.String, nullable=True)
    dinh_kem_chung_nhan_da_cap = db.Column(db.String, nullable=True)
    ly_do_tu_choi = db.Column(db.String, nullable=True)
    ma_nguoi_tu_choi = db.Column(db.String, nullable=True)
    ten_nguoi_tu_choi = db.Column(db.String, nullable=True)
    thoi_gian_tu_choi = db.Column(db.String, nullable=True)
    thoi_gian_thu_ly = db.Column(db.String, nullable=True)
    ngay_het_han_ho_so = db.Column(db.String, nullable=True)
    thoi_gian_nop_ho_so = db.Column(db.String, nullable=True)
    thoi_gian_in_du_thao = db.Column(db.String, nullable=True)
    thoi_gian_in_tham_xet = db.Column(db.String, nullable=True)
    thoi_gian_in_chung_chi = db.Column(db.String, nullable=True)
    thoi_gian_lanh_dao_duyet = db.Column(db.String, nullable=True)
    trang_thai = db.Column(db.String, nullable=True)
    # danh_muc_kinh_doanh =db.Column(db.JSON, nullable=True)
    so_dan_chieu = db.Column(db.String, nullable=True)
    ket_qua_tham_xet = db.Column(db.String, nullable=True)

    pham_vi_kinh_doanh = db.Column(JSONB, nullable=True)

    thu_tuc = db.relationship("DanhMucThuTuc", foreign_keys=[
                              thu_tuc_id], backref="yeu_cau_dang_ky_kinh_doanh",  lazy="joined")
    co_so_kinh_doanh = db.relationship(
        "CoSoKinhDoanh", foreign_keys=[co_so_kinh_doanh_id], backref="yeu_cau_dang_ky_kinh_doanh", lazy="joined")

    def __init__(
        self,
        co_so_kinh_doanh_id=None,
        thong_tin_co_so_kinh_doanh=None,
        ten_co_so=None,
        loai_yeu_cau=None,
        thu_tuc_id=None,
        ma_thu_tuc_bo_sung=None,
        ngay_nop_ho_so=None,
        ngay_het_han_ho_so=None,
        co_quan_cap=None,
        ngay_cap=None,
        ngay_hieu_luc=None,
        ngay_het_han=None,
        lan_cap_thu=None,
        so_chung_chi_moi=None,
        loai_ma_chung_chi=None,
        thay_the_chung_chi=None,
        hoi_dong_id=None,
        so_quyet_dinh=None,
        ngay_quyet_dinh=None,
        loai_ma_chung_chi_gps=None,
        so_chung_nhan_gps=None,
        ngay_cap_gps=None,
        ngay_het_han_gps=None,
        danh_sach_chung_nhan_gps=None,
        danh_sach_chung_nhan_kinh_doanh=None,
        danh_sach_nguoi_hanh_nghe=None,
        ly_do_cap_lai=None,
        noi_dung_dieu_chinh=None,
        noi_dung_tham_xet=None,
        noi_dung_de_nghi=None,
        noi_dung_yeu_cau=None,
        ma_nguoi_cap_nhat=None,
        ten_nguoi_cap_nhat=None,
        thoi_gian_cap_nhat=None,
        ma_nguoi_thu_ly=None,
        ten_nguoi_thu_ly=None,
        nguoi_thu_ly=None,
        y_kien_lanh_dao=None,
        dinh_kem_don_de_nghi=None,
        dinh_kem_chung_chi_da_cap=None,
        dinh_kem_cchnd_thay_doi=None,
        dinh_kem_cndkkdd_gps=None,
        dinh_kem_so_do_nhansu=None,
        dinh_kem_so_do_co_so=None,
        dinh_kem_trang_thiet_bi=None,
        dinh_kem_ho_so=None,
        dinh_kem_kiem_tra_thuc_hanh=None,
        dinh_kem_chung_nhan_co_so=None,
        dinh_kem_chung_chi_hanh_nghe=None,
        dinh_kem_tai_lieu_thuyet_minh=None,
        dinh_kem_xac_nhan_le_phi=None,
        dinh_kem_files_khac=None,
        dinh_kem_chung_nhan_bi_sai=None,
        dinh_kem_ban_sao_cchnd=None,
        dinh_kem_chung_nhan_dang_ky_doanh_nghiep=None,
        dinh_kem_chung_nhan_da_cap=None,
        ly_do_tu_choi=None,
        ma_nguoi_tu_choi=None,
        ten_nguoi_tu_choi=None,
        thoi_gian_tu_choi=None,
        thoi_gian_thu_ly=None,
        thoi_gian_nop_ho_so=None,
        thoi_gian_in_du_thao=None,
        thoi_gian_in_tham_xet=None,
        thoi_gian_in_chung_chi=None,
        thoi_gian_lanh_dao_duyet=None,
        trang_thai=None,
        so_dan_chieu=None,
        ket_qua_tham_xet=None,
        pham_vi_kinh_doanh=None,
    ):
        self.id = uuid.uuid4()
        self.so_chung_nhan_gps = so_chung_nhan_gps
        self.co_so_kinh_doanh_id = co_so_kinh_doanh_id
        self.thong_tin_co_so_kinh_doanh = thong_tin_co_so_kinh_doanh
        self.ten_co_so = ten_co_so
        self.ten_co_so_khong_dau = clean_string(ten_co_so)
        self.loai_yeu_cau = loai_yeu_cau
        self.thu_tuc_id = thu_tuc_id
        self.ma_thu_tuc_bo_sung = ma_thu_tuc_bo_sung
        self.ngay_nop_ho_so = ngay_nop_ho_so
        self.ngay_het_han_ho_so = ngay_het_han_ho_so
        self.co_quan_cap = co_quan_cap
        self.ngay_cap = ngay_cap
        self.ngay_hieu_luc = ngay_hieu_luc
        self.ngay_het_han = ngay_het_han
        self.lan_cap_thu = lan_cap_thu
        self.so_chung_chi_moi = so_chung_chi_moi
        self.loai_ma_chung_chi = loai_ma_chung_chi
        self.thay_the_chung_chi = thay_the_chung_chi
        self.hoi_dong_id = hoi_dong_id
        self.so_quyet_dinh = so_quyet_dinh
        self.ngay_quyet_dinh = ngay_quyet_dinh
        self.loai_ma_chung_chi_gps = loai_ma_chung_chi_gps
        self.ngay_cap_gps = ngay_cap_gps
        self.ngay_het_han_gps = ngay_het_han_gps
        self.danh_sach_chung_nhan_gps = danh_sach_chung_nhan_gps
        self.danh_sach_chung_nhan_kinh_doanh = danh_sach_chung_nhan_kinh_doanh
        self.danh_sach_nguoi_hanh_nghe = danh_sach_nguoi_hanh_nghe
        self.ly_do_cap_lai = ly_do_cap_lai
        self.noi_dung_dieu_chinh = noi_dung_dieu_chinh
        self.noi_dung_tham_xet = noi_dung_tham_xet
        self.noi_dung_de_nghi = noi_dung_de_nghi
        self.noi_dung_yeu_cau = noi_dung_yeu_cau
        self.ma_nguoi_cap_nhat = ma_nguoi_cap_nhat
        self.ten_nguoi_cap_nhat = ten_nguoi_cap_nhat
        self.thoi_gian_cap_nhat = thoi_gian_cap_nhat
        self.ma_nguoi_thu_ly = ma_nguoi_thu_ly
        self.ten_nguoi_thu_ly = ten_nguoi_thu_ly
        self.nguoi_thu_ly = nguoi_thu_ly
        self.y_kien_lanh_dao = y_kien_lanh_dao
        self.dinh_kem_don_de_nghi = dinh_kem_don_de_nghi
        self.dinh_kem_chung_chi_da_cap = dinh_kem_chung_chi_da_cap
        self.dinh_kem_cchnd_thay_doi = dinh_kem_cchnd_thay_doi
        self.dinh_kem_cndkkdd_gps = dinh_kem_cndkkdd_gps
        self.dinh_kem_so_do_nhansu = dinh_kem_so_do_nhansu
        self.dinh_kem_so_do_co_so = dinh_kem_so_do_co_so
        self.dinh_kem_trang_thiet_bi = dinh_kem_trang_thiet_bi
        self.dinh_kem_ho_so = dinh_kem_ho_so
        self.dinh_kem_kiem_tra_thuc_hanh = dinh_kem_kiem_tra_thuc_hanh
        self.dinh_kem_chung_nhan_co_so = dinh_kem_chung_nhan_co_so
        self.dinh_kem_chung_chi_hanh_nghe = dinh_kem_chung_chi_hanh_nghe
        self.dinh_kem_tai_lieu_thuyet_minh = dinh_kem_tai_lieu_thuyet_minh
        self.dinh_kem_xac_nhan_le_phi = dinh_kem_xac_nhan_le_phi
        self.dinh_kem_files_khac = dinh_kem_files_khac
        self.dinh_kem_chung_nhan_bi_sai = dinh_kem_chung_nhan_bi_sai
        self.dinh_kem_ban_sao_cchnd = dinh_kem_ban_sao_cchnd
        self.dinh_kem_chung_nhan_dang_ky_doanh_nghiep = dinh_kem_chung_nhan_dang_ky_doanh_nghiep
        self.dinh_kem_chung_nhan_da_cap = dinh_kem_chung_nhan_da_cap
        self.ly_do_tu_choi = ly_do_tu_choi
        self.ma_nguoi_tu_choi = ma_nguoi_tu_choi
        self.ten_nguoi_tu_choi = ten_nguoi_tu_choi
        self.thoi_gian_tu_choi = thoi_gian_tu_choi
        self.thoi_gian_thu_ly = thoi_gian_thu_ly
        self.thoi_gian_nop_ho_so = thoi_gian_nop_ho_so
        self.thoi_gian_in_du_thao = thoi_gian_in_du_thao
        self.thoi_gian_in_tham_xet = thoi_gian_in_tham_xet
        self.thoi_gian_in_chung_chi = thoi_gian_in_chung_chi
        self.thoi_gian_lanh_dao_duyet = thoi_gian_lanh_dao_duyet
        self.trang_thai = trang_thai
        self.so_dan_chieu = so_dan_chieu
        self.ket_qua_tham_xet = ket_qua_tham_xet
        self.pham_vi_kinh_doanh = pham_vi_kinh_doanh


@event.listens_for(YeuCauDangKyKinhDoanh, "before_insert")
def on_insert_trigger(mapper, connection, target):
    verify_jwt_in_request()
    target.created_at = datetime.now()
    target.created_by = current_user.id


@event.listens_for(YeuCauDangKyKinhDoanh, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.now()
