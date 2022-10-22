from application.commons.commons import CommonModel
from application.extensions import db
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import backref
import uuid

from application.utils.helper.string_processing_helper import clean_string

class BangCap(CommonModel):

    __tablename__="bang_cap"
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    nhan_vien_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"), nullable=True)
    van_bang_chuyen_mon_id = db.Column(UUID(as_uuid=True), db.ForeignKey("danhmuc_van_bang_chuyen_mon.id"), nullable=True)
    so_hieu = db.Column(db.String,nullable=True)
    loai_hinh_dao_tao = db.Column(db.String,nullable=True)
    noi_tot_nghiep_id = db.Column(UUID(as_uuid=True), db.ForeignKey("danhmuc_noi_tot_nghiep.id"), nullable=True)
    nganh_dao_tao = db.Column(db.String,nullable=True)
    xep_hang = db.Column(db.String,nullable=True)
    danh_hieu = db.Column(db.String,nullable=True)
    ngay_cap = db.Column(db.BigInteger, nullable=True)
    trang_thai = db.Column(db.String, default=True)
    chung_tu_dinh_kem = db.Column(MutableList.as_mutable(JSONB), default=[], nullable=True)
    hinh_thuc_dao_tao = db.Column(db.String, nullable=True)
    nam_cap = db.Column(db.String, nullable=True)
    ghi_chu = db.Column(db.TEXT,nullable=True)

    noi_tot_nghiep = db.relationship("NoiTotNghiep", backref=backref("bang_cap",lazy="dynamic"))
    van_bang_chuyen_mon = db.relationship("VanBangChuyenMon", backref=backref("bang_cap",lazy="dynamic"))
    nhan_vien = db.relationship("User", foreign_keys=[nhan_vien_id], back_populates="bang_cap")

    def __init__(self, nhan_vien_id=None,
                 trang_thai=None, van_bang_chuyen_mon_id=None, so_hieu=None, loai_hinh_dao_tao=None,
                 noi_tot_nghiep_id=None, nganh_dao_tao=None, xep_hang=None, danh_hieu=None, ngay_cap=None, chung_tu_dinh_kem=[],
                 ghi_chu=None,hinh_thuc_dao_tao=None,nam_cap=None):
        self.id = uuid.uuid4()
        self.nhan_vien_id = nhan_vien_id
        self.trang_thai = trang_thai
        self.van_bang_chuyen_mon_id = van_bang_chuyen_mon_id
        self.so_hieu = so_hieu
        self.loai_hinh_dao_tao = loai_hinh_dao_tao
        self.noi_tot_nghiep_id = noi_tot_nghiep_id
        self.nganh_dao_tao = nganh_dao_tao
        self.xep_hang = xep_hang
        self.danh_hieu = danh_hieu
        self.ngay_cap = ngay_cap
        self.chung_tu_dinh_kem = chung_tu_dinh_kem
        self.ghi_chu = ghi_chu
        self.hinh_thuc_dao_tao = hinh_thuc_dao_tao
        self.nam_cap = nam_cap

        