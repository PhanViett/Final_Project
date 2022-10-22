import datetime
from application.commons.commons import CommonModel
from application.extensions import db
import uuid
from sqlalchemy import event

from sqlalchemy.dialects.postgresql import UUID
from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.generate_so_thu_tu import generate_number
def generate_ma_ho_so():
    so_thu_tu = generate_number("danhmuc_thu_tuc")
    data = "TT" + str(so_thu_tu).zfill(3)
    return data
class DanhMucThuTuc(CommonModel):

    __tablename__ = "danhmuc_thu_tuc"

    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    loai_thu_tuc = db.Column(db.String,nullable=True)
    ma_thu_tuc = db.Column(db.String,nullable=True)
    ten = db.Column(db.String,nullable=True)
    ten_khong_dau = db.Column(db.String,nullable=True)
    linh_vuc = db.Column(db.String,nullable=True)
    muc_do = db.Column(db.String, nullable=True)
    doi_tuong = db.Column(db.String, nullable=True)
    co_quan_thuc_hien = db.Column(db.String, nullable=True)
    thoi_gian_thuc_hien_bang_so = db.Column(db.String, nullable=True)
    thoi_gian_giai_quyet = db.Column(db.String, nullable=True)
    ket_qua_thuc_hien = db.Column(db.String, nullable=True)
    le_phi_text = db.Column(db.String, nullable=True)
    le_phi_number = db.Column(db.String, nullable=True)
    cach_thuc_hien = db.Column(db.String, nullable=True)
    thanh_phan_ho_so = db.Column(db.String, nullable=True)
    can_cu_phap_ly = db.Column(db.String, nullable=True)
    trang_thai = db.Column(db.Boolean,nullable=True)
    
    
    ho_so = db.relationship("ThanhPhanHoSo",lazy="joined", back_populates="thu_tuc")

    def __init__(
        self,
        loai_thu_tuc = None,
        ma_thu_tuc= None, 
        ten= None, 
        linh_vuc =None,
        muc_do=None,
        doi_tuong=None,
        co_quan_thuc_hien = None,
        thoi_gian_thuc_hien_bang_so = None,
        thoi_gian_giai_quyet = None,
        ket_qua_thuc_hien = None,
        le_phi_text = None,
        le_phi_number = None,
        cach_thuc_hien = None,
        thanh_phan_ho_so = None,
        can_cu_phap_ly = None,
        trang_thai = None,
    ):
        self.id = uuid.uuid4()
        self.loai_thu_tuc = loai_thu_tuc
        self.ma_thu_tuc = generate_ma_ho_so()
        self.ten = ten
        self.ten_khong_dau =clean_string(ten)
        self.linh_vuc = linh_vuc       
        self.muc_do = muc_do
        self.doi_tuong= doi_tuong
        self.co_quan_thuc_hien = co_quan_thuc_hien
        self.thoi_gian_thuc_hien_bang_so = thoi_gian_thuc_hien_bang_so
        self.thoi_gian_giai_quyet = thoi_gian_giai_quyet
        self.ket_qua_thuc_hien = ket_qua_thuc_hien
        self.le_phi_text = le_phi_text
        self.le_phi_number = le_phi_number
        self.cach_thuc_hien = cach_thuc_hien
        self.thanh_phan_ho_so = thanh_phan_ho_so
        self.can_cu_phap_ly = can_cu_phap_ly
        self.trang_thai = trang_thai
@event.listens_for(DanhMucThuTuc, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(DanhMucThuTuc, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()  