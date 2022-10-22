from datetime import datetime
from enum import unique
import json
from application.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from application.commons.commons import CommonModel
from application.extensions import db
from sqlalchemy import ForeignKey, event
from flask_jwt_extended import current_user
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from application.utils.helper.generate_so_thu_tu import generate_number
from sqlalchemy.ext.mutable import MutableList


def generate_ma_ho_so():
    so_thu_tu = generate_number("yeu_cau_cchnd")
    data = "HS" + str(so_thu_tu).zfill(7)
    return data


class YeuCauChungChiHanhNghe(CommonModel):

    __tablename__ = "yeu_cau_chung_chi_hanh_nghe"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nhan_vien_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"), nullable=True)
    lanh_dao_duyet_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"), nullable=True)
    nhan_vien_thu_ly_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"), nullable=True)
    chung_chi_id = db.Column(UUID(as_uuid=True), db.ForeignKey("chung_chi_hanh_nghe.id"), nullable=True)
    thu_tuc_id = db.Column(UUID(as_uuid=True), db.ForeignKey("danhmuc_thu_tuc.id"), nullable=True)
    thu_tuc_bo_sung_id = db.Column(UUID(as_uuid=True), db.ForeignKey("danhmuc_thu_tuc.id"), nullable=True)
    hoi_dong_id = db.Column(UUID(as_uuid=True), db.ForeignKey("danhmuc_hoi_dong.id"), nullable=True)
    ma_ho_so = db.Column(db.String, unique=True, nullable=True)
    doi_tuong = db.Column(MutableDict.as_mutable(JSONB), nullable=True)
    loai_yeu_cau = db.Column(db.String, nullable=True)
    loai_cap_chung_chi = db.Column(db.String, nullable=True)
    lan_cap_thu = db.Column(db.String, nullable=True)
    so_cchnd = db.Column(db.String, nullable=True)
    ngay_hieu_luc = db.Column(db.BigInteger)
    ngay_het_han = db.Column(db.BigInteger)
    thay_the_cchnd = db.Column(db.String, nullable=True)
    ngay_cap_cchnd_cu = db.Column(db.BigInteger, nullable=True)
    hinh_thuc = db.Column(db.String, nullable=True)
    yeu_cau_phien_dich = db.Column(db.Boolean, nullable=True)
    so_quyet_dinh = db.Column(db.String, nullable=True)
    ngay_quyet_dinh = db.Column(db.BigInteger, nullable=True)
    ly_do_mat_hong = db.Column(db.TEXT, nullable=True)
    noi_dung_dieu_chinh = db.Column(db.TEXT, nullable=True)
    noi_dung_tham_xet = db.Column(db.TEXT, nullable=True)
    noi_dung_de_nghi = db.Column(db.TEXT, nullable=True)
    noi_dung_yeu_cau_bo_sung_chuyen_vien = db.Column(db.TEXT, nullable=True)
    noi_dung_yeu_cau_bo_sung_lanh_dao = db.Column(db.TEXT, nullable=True)
    y_kien_lanh_dao = db.Column(MutableList.as_mutable(db.JSON), nullable=True)
    dinh_kem_chung_chi = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    dinh_kem_don_de_nghi = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    dinh_kem_anh_chan_dung = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    dinh_kem_van_bang_chuyen_mon = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    dinh_kem_xac_nhan_suc_khoe = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    dinh_kem_xac_nhan_thuc_hanh = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    dinh_kem_xac_nhan_dao_tao = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    dinh_kem_xac_nhan_cong_dan = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    dinh_kem_xac_nhan_ly_lich = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    dinh_kem_xac_nhan_cam_ket = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    dinh_kem_xac_nhan_le_phi = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    dinh_kem_xac_nhan_thay_doi = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    dinh_kem_xac_nhan_files = db.Column(MutableList.as_mutable(db.JSON), default=[], nullable=True)
    trang_thai_ho_so = db.Column(db.String, nullable=True)
    ly_do_tu_choi_chuyen_vien = db.Column(db.String, nullable=True)
    ly_do_tu_choi_lanh_dao = db.Column(db.String, nullable=True)
    thoi_gian_thu_ly = db.Column(db.BigInteger, nullable=True)
    ngay_het_han_ho_so = db.Column(db.BigInteger, nullable=True)
    loai_ma_cchnd = db.Column(UUID(as_uuid=True), db.ForeignKey("loai_ma_chung_chi.id"), nullable=True)
    thoi_gian_in_chung_chi = db.Column(db.BigInteger, nullable=True)
    thoi_gian_in_tham_xet = db.Column(db.BigInteger, nullable=True)
    thoi_gian_lanh_dao_duyet = db.Column(db.BigInteger, nullable=True)
    thoi_gian_nop_ho_so = db.Column(db.BigInteger, nullable=True)
    trang_thai_het_han = db.Column(db.Boolean, default=True, nullable=True)
    confirm = db.Column(db.Boolean, default=False, nullable=True)

    pham_vi_chuyen_mon = db.Column(JSONB, nullable=True)

    vi_tri_hanh_nghe_cchn = db.Column(JSONB, nullable=True)

    thu_tuc = db.relationship("DanhMucThuTuc", foreign_keys=[
                              thu_tuc_id], backref="yeu_cau_chung_chi_hanh_nghe",  lazy="joined")
    duoc_si = db.relationship("User", foreign_keys=[nhan_vien_id], backref="yeu_cau_chung_chi_hanh_nghe", lazy="joined")

    def __init__(
        self,
        nhan_vien_id=None,
        doi_tuong=None,
        chung_chi_id=None,
        thu_tuc_id=None,
        thu_tuc_bo_sung_id=None,
        hoi_dong_id=None,
        loai_yeu_cau=None,
        loai_cap_chung_chi=None,
        hinh_thuc=None,
        lan_cap_thu=None,
        so_cchnd=None,
        thay_the_cchnd=None,
        yeu_cau_phien_dich=None,
        so_quyet_dinh=None,
        ngay_quyet_dinh=None,
        ly_do_mat_hong=None,
        noi_dung_dieu_chinh=None,
        noi_dung_tham_xet=None,
        noi_dung_de_nghi=None,
        noi_dung_yeu_cau_bo_sung_chuyen_vien=None,
        noi_dung_yeu_cau_bo_sung_lanh_dao=None,
        y_kien_lanh_dao=None,
        dinh_kem_chung_chi=[],
        dinh_kem_don_de_nghi=[],
        dinh_kem_anh_chan_dung=[],
        dinh_kem_van_bang_chuyen_mon=[],
        dinh_kem_xac_nhan_suc_khoe=[],
        dinh_kem_xac_nhan_thuc_hanh=[],
        dinh_kem_xac_nhan_dao_tao=[],
        dinh_kem_xac_nhan_cong_dan=[],
        dinh_kem_xac_nhan_ly_lich=[],
        dinh_kem_xac_nhan_cam_ket=[],
        dinh_kem_xac_nhan_le_phi=[],
        dinh_kem_xac_nhan_thay_doi=[],
        dinh_kem_xac_nhan_files=[],
        trang_thai_ho_so=None,
        ly_do_tu_choi_chuyen_vien=None,
        ly_do_tu_choi_lanh_dao=None,
        thoi_gian_thu_ly=None,
        ngay_het_han_ho_so=None,
        loai_ma_cchnd=None,
        pham_vi_chuyen_mon=None,
        vi_tri_hanh_nghe_cchn=None,
        thoi_gian_in_chung_chi=None,
        thoi_gian_in_tham_xet=None,
        thoi_gian_lanh_dao_duyet=None,
        thoi_gian_nop_ho_so=None,
        trang_thai_het_han=None,
        ngay_hieu_luc=None,
        ngay_het_han=None,
        ngay_cap_cchnd_cu=None,
        confirm=False
    ):
        self.id = uuid.uuid4()
        self.nhan_vien_id = nhan_vien_id
        self.doi_tuong = doi_tuong
        self.chung_chi_id = chung_chi_id
        self.thu_tuc_id = thu_tuc_id,
        self.thu_tuc_bo_sung_id = thu_tuc_bo_sung_id,
        self.hoi_dong_id = hoi_dong_id,
        self.ma_ho_so = generate_ma_ho_so()
        self.loai_yeu_cau = loai_yeu_cau
        self.loai_cap_chung_chi = loai_cap_chung_chi
        self.hinh_thuc = hinh_thuc
        self.lan_cap_thu = lan_cap_thu
        self.so_cchnd = so_cchnd
        self.thay_the_cchnd = thay_the_cchnd
        self.yeu_cau_phien_dich = yeu_cau_phien_dich
        self.so_quyet_dinh = so_quyet_dinh
        self.ngay_quyet_dinh = ngay_quyet_dinh
        self.ly_do_mat_hong = ly_do_mat_hong
        self.noi_dung_dieu_chinh = noi_dung_dieu_chinh
        self.noi_dung_tham_xet = noi_dung_tham_xet
        self.noi_dung_de_nghi = noi_dung_de_nghi
        self.noi_dung_yeu_cau_bo_sung_chuyen_vien = noi_dung_yeu_cau_bo_sung_chuyen_vien
        self.noi_dung_yeu_cau_bo_sung_lanh_dao = noi_dung_yeu_cau_bo_sung_lanh_dao
        self.y_kien_lanh_dao = y_kien_lanh_dao
        self.dinh_kem_chung_chi = dinh_kem_chung_chi
        self.dinh_kem_don_de_nghi = dinh_kem_don_de_nghi
        self.dinh_kem_anh_chan_dung = dinh_kem_anh_chan_dung
        self.dinh_kem_van_bang_chuyen_mon = dinh_kem_van_bang_chuyen_mon
        self.dinh_kem_xac_nhan_suc_khoe = dinh_kem_xac_nhan_suc_khoe
        self.dinh_kem_xac_nhan_thuc_hanh = dinh_kem_xac_nhan_thuc_hanh
        self.dinh_kem_xac_nhan_dao_tao = dinh_kem_xac_nhan_dao_tao
        self.dinh_kem_xac_nhan_cong_dan = dinh_kem_xac_nhan_cong_dan
        self.dinh_kem_xac_nhan_ly_lich = dinh_kem_xac_nhan_ly_lich
        self.dinh_kem_xac_nhan_cam_ket = dinh_kem_xac_nhan_cam_ket
        self.dinh_kem_xac_nhan_le_phi = dinh_kem_xac_nhan_le_phi
        self.dinh_kem_xac_nhan_thay_doi = dinh_kem_xac_nhan_thay_doi
        self.dinh_kem_xac_nhan_files = dinh_kem_xac_nhan_files
        self.trang_thai_ho_so = trang_thai_ho_so
        self.ly_do_tu_choi_chuyen_vien = ly_do_tu_choi_chuyen_vien
        self.ly_do_tu_choi_lanh_dao = ly_do_tu_choi_lanh_dao
        self.thoi_gian_thu_ly = thoi_gian_thu_ly
        self.ngay_het_han_ho_so = ngay_het_han_ho_so
        self.loai_ma_cchnd = loai_ma_cchnd
        self.pham_vi_chuyen_mon = pham_vi_chuyen_mon
        self.vi_tri_hanh_nghe_cchn = vi_tri_hanh_nghe_cchn
        self.thoi_gian_in_chung_chi = thoi_gian_in_chung_chi
        self.thoi_gian_in_tham_xet = thoi_gian_in_tham_xet
        self.thoi_gian_lanh_dao_duyet = thoi_gian_lanh_dao_duyet
        self.thoi_gian_nop_ho_so = thoi_gian_nop_ho_so
        self.trang_thai_het_han = trang_thai_het_han
        self.ngay_hieu_luc = ngay_hieu_luc
        self.ngay_het_han = ngay_het_han
        self.ngay_cap_cchnd_cu = ngay_cap_cchnd_cu
        self.confirm = confirm


@event.listens_for(YeuCauChungChiHanhNghe, "before_insert")
def on_insert_trigger(mapper, connection, target):
    verify_jwt_in_request()
    target.created_at = datetime.now()
    target.created_by = current_user.id


@event.listens_for(YeuCauChungChiHanhNghe, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.now()
