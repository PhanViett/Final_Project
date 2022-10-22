from application.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime
from application.commons.commons import CommonModel
from application.extensions import db
from flask_jwt_extended import current_user
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList

from sqlalchemy import event
class CoSoThucHanh(CommonModel):

    __tablename__="co_so_thuc_hanh"
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    nhan_vien_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"), nullable=True)
    ma_co_so = db.Column(db.String, nullable=True)
    giay_chung_nhan = db.Column(db.String, nullable=True)
    ten_co_so = db.Column(db.String, nullable=True)
    dia_chi_co_so = db.Column(db.String, nullable=True)
    tu_ngay = db.Column(db.BigInteger, nullable=True)
    den_ngay = db.Column(db.BigInteger, nullable=True)
    chung_tu_dinh_kem = db.Column(MutableList.as_mutable(JSONB), default=[], nullable=True)
    trang_thai = db.Column(db.String, nullable=True) 
    ten_nguoi_phu_trach = db.Column(db.String, nullable=True)
    dien_thoai_nguoi_phu_trach = db.Column(db.String, nullable=True)
    noi_dung_khac = db.Column(db.TEXT, nullable=True)
    so_nha = db.Column(db.String, nullable=True)
    quan_huyen_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quan_huyen.id"), nullable=True)
    tinh_thanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tinh_thanh.id"), nullable=True)
    xa_phuong_id = db.Column(UUID(as_uuid=True), db.ForeignKey("xa_phuong.id"), nullable=True)
    noi_dung_thuc_hanh= db.Column(MutableList.as_mutable(JSONB), default=[], nullable=True)


    tinh_thanh = db.relationship("TinhThanh", foreign_keys=[tinh_thanh_id], uselist=False)
    quan_huyen = db.relationship("QuanHuyen", foreign_keys=[quan_huyen_id], uselist=False)
    xa_phuong = db.relationship("XaPhuong", foreign_keys=[xa_phuong_id], uselist=False) 

    def __init__(self, 
                 nhan_vien_id = None, 
                 ma_co_so = None, 
                 giay_chung_nhan =None,
                 ten_co_so = None,
                 dia_chi_co_so = None,
                 tu_ngay = None,
                 den_ngay = None,
                 chung_tu_dinh_kem =[],
                 trang_thai =  None,
                 ten_nguoi_phu_trach = None,
                 dien_thoai_nguoi_phu_trach = None,
                 noi_dung_khac = None,
                 so_nha = None,
                 quan_huyen_id = None,
                 tinh_thanh_id = None,
                 xa_phuong_id = None,
                 noi_dung_thuc_hanh = None):

                 self.id = uuid.uuid4()
                 self.nhan_vien_id = nhan_vien_id
                 self.ma_co_so = ma_co_so
                 self.giay_chung_nhan =giay_chung_nhan
                 self.ten_co_so = ten_co_so
                 self.dia_chi_co_so = dia_chi_co_so
                 self.tu_ngay = tu_ngay
                 self.den_ngay = den_ngay
                 self.chung_tu_dinh_kem = chung_tu_dinh_kem
                 self.trang_thai = trang_thai
                 self.ten_nguoi_phu_trach = ten_nguoi_phu_trach
                 self.dien_thoai_nguoi_phu_trach = dien_thoai_nguoi_phu_trach
                 self.noi_dung_khac = noi_dung_khac
                 self.so_nha = so_nha
                 self.quan_huyen_id = quan_huyen_id
                 self.tinh_thanh_id = tinh_thanh_id
                 self.xa_phuong_id = xa_phuong_id
                 self.noi_dung_thuc_hanh = noi_dung_thuc_hanh
@event.listens_for(CoSoThucHanh, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(CoSoThucHanh, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()
