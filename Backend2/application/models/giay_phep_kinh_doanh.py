
import datetime
from sqlalchemy import event
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList
from flask_jwt_extended import current_user, verify_jwt_in_request
from application.commons.commons import CommonModel
from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from application.utils.helper.string_processing_helper import clean_string

lk_loai_hinh_kinh_doanh_giay_phep = db.Table(
    "lk_loai_hinh_kinh_doanh_giay_phep", db.Model.metadata,
    db.Column("loai_hinh_kd_id", UUID(as_uuid=True),  db.ForeignKey(
        'danhmuc_loai_hinh_kinh_doanh.id'), primary_key=True),
    db.Column("giay_phep_id", UUID(as_uuid=True),  db.ForeignKey('giay_phep_kinh_doanh.id'), primary_key=True))

lk_pham_vi_kinh_doanh_giay_phep = db.Table(
    "lk_pham_vi_kinh_doanh_giay_phep", db.Model.metadata,
    db.Column("pham_vi_kd_id", UUID(as_uuid=True),  db.ForeignKey(
        'danhmuc_pham_vi_hoat_dong_kinh_doanh.id'), primary_key=True),
    db.Column("giay_phep_id", UUID(as_uuid=True),  db.ForeignKey('giay_phep_kinh_doanh.id'), primary_key=True))


class GiayPhepKinhDoanh(CommonModel):

    __tablename__ = "giay_phep_kinh_doanh"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    so_giay_phep = db.Column(db.String, nullable=True)
    ngay_cap = db.Column(db.BigInteger, nullable=True)
    ngay_hieu_luc = db.Column(db.BigInteger, nullable=True)
    ngay_het_han = db.Column(db.BigInteger, nullable=True)
    co_quan_cap = db.Column(db.String, nullable=True)
    so_giay_gps = db.Column(db.String, nullable=True)
    co_so_kinh_doanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("co_so_kinh_doanh.id"), nullable=True)

    thoigian_yeucau_lienket = db.Column(db.BigInteger, nullable=True)
    thoigian_duyet_lienket = db.Column(db.BigInteger, nullable=True)
    thoigian_tuchoi_lienket = db.Column(db.BigInteger, nullable=True)
    lydo_tuchoi_lienket = db.Column(db.String, nullable=True)
    ma_nguoiduyet = db.Column(db.String, nullable=True)
    ten_nguoiduyet = db.Column(db.String, nullable=True)
    trang_thai_ho_so = db.Column(db.String, nullable=True, default='0')

    tinh_thanh_kinh_doanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tinh_thanh.id"), nullable=True)
    quan_huyen_kinh_doanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quan_huyen.id"), nullable=True)
    xa_phuong_kinh_doanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("xa_phuong.id"), nullable=True)

    ghi_chu = db.Column(db.String, nullable=True)
    ghi_chu_loai_hinh_kd = db.Column(db.String, nullable=True)
    ghi_chu_pham_vi_kd = db.Column(db.String, nullable=True)
    ten_httckd = db.Column(db.String, nullable=True)
    ten_tru_so = db.Column(db.String, nullable=True)
    dia_chi_tru_so = db.Column(db.String, nullable=True)

    dinh_kem_chung_chi = db.Column(MutableList.as_mutable(JSONB), default=[], nullable=True)
    dinh_kem_anh_chan_dung = db.Column(MutableList.as_mutable(JSONB), default=[], nullable=True)
    dinh_kem_van_bang_chuyen_mon = db.Column(MutableList.as_mutable(JSONB), default=[], nullable=True)
    dinh_kem_xac_nhan_cong_dan = db.Column(MutableList.as_mutable(JSONB), default=[], nullable=True)
    dinh_kem_files_khac = db.Column(MutableList.as_mutable(JSONB), default=[], nullable=True)

    tinh_thanh = db.relationship("TinhThanh", foreign_keys=[tinh_thanh_kinh_doanh_id], uselist=False)
    quan_huyen = db.relationship("QuanHuyen", foreign_keys=[quan_huyen_kinh_doanh_id], uselist=False)
    xa_phuong = db.relationship("XaPhuong", foreign_keys=[xa_phuong_kinh_doanh_id], uselist=False)

    loai_hinh_kinh_doanh = db.relationship("LoaiHinhKinhDoanh", secondary="lk_loai_hinh_kinh_doanh_giay_phep",
                                           cascade="delete", backref=db.backref("giay_phep_kinh_doanh", lazy=True))
    pham_vi_kinh_doanh = db.relationship("PhamViHoatDongKinhDoanh", secondary="lk_pham_vi_kinh_doanh_giay_phep",
                                         cascade="delete", backref=db.backref("giay_phep_kinh_doanh", lazy=True))
    co_so_kinh_doanh = db.relationship("CoSoKinhDoanh", foreign_keys=[
                                       co_so_kinh_doanh_id], back_populates="giay_phep_kinh_doanh")

    def __init__(
        self,
        so_giay_phep=None,
        so_giay_phep_before=None,
        so_giay_phep_after=None,
        ngay_cap=None,
        ngay_hieu_luc=None,
        ngay_het_han=None,
        co_quan_cap=None,
        so_giay_gps=None,
        tinh_thanh_kinh_doanh_id=None,
        quan_huyen_kinh_doanh_id=None,
        xa_phuong_kinh_doanh_id=None,
        ghi_chu=None,
        ghi_chu_loai_hinh_kd=None,
        ghi_chu_pham_vi_kd=None,
        ten_tru_so=None,
        ten_httckd=None,
        thoigian_yeucau_lienket=None,
        thoigian_duyet_lienket=None,
        thoigian_tuchoi_lienket=None,
        lydo_tuchoi_lienket=None,
        ma_nguoiduyet=None,
        ten_nguoiduyet=None,
        dia_chi_tru_so=None,
        trang_thai_ho_so=None,
        co_so_kinh_doanh_id=None,
    ):
        self.so_giay_phep = so_giay_phep
        self.so_giay_phep_before = so_giay_phep_before
        self.so_giay_phep_after = so_giay_phep_after
        self.ngay_cap = ngay_cap
        self.ngay_hieu_luc = ngay_hieu_luc
        self.ngay_het_han = ngay_het_han
        self.co_quan_cap = co_quan_cap
        self.so_giay_gps = so_giay_gps
        self.tinh_thanh_kinh_doanh_id = tinh_thanh_kinh_doanh_id
        self.quan_huyen_kinh_doanh_id = quan_huyen_kinh_doanh_id
        self.xa_phuong_kinh_doanh_id = xa_phuong_kinh_doanh_id
        self.ghi_chu = ghi_chu
        self.ghi_chu_loai_hinh_kd = ghi_chu_loai_hinh_kd
        self.ghi_chu_pham_vi_kd = ghi_chu_pham_vi_kd
        self.ten_tru_so = ten_tru_so
        self.ten_httckd = ten_httckd
        self.thoigian_yeucau_lienket = thoigian_yeucau_lienket
        self.thoigian_duyet_lienket = thoigian_duyet_lienket
        self.thoigian_tuchoi_lienket = thoigian_tuchoi_lienket
        self.ma_nguoiduyet = ma_nguoiduyet
        self.ten_nguoiduyet = ten_nguoiduyet
        self.dia_chi_tru_so = dia_chi_tru_so
        self.lydo_tuchoi_lienket = lydo_tuchoi_lienket
        self.trang_thai_ho_so = trang_thai_ho_so
        self.co_so_kinh_doanh_id = co_so_kinh_doanh_id


@event.listens_for(GiayPhepKinhDoanh, "before_insert")
def on_update_trigger(mapper, connection, target):
    verify_jwt_in_request()
    target.updated_at = datetime.datetime.now()
    target.created_by = current_user.id


@event.listens_for(GiayPhepKinhDoanh, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()
    target.update_by = current_user.id
