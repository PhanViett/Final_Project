
import datetime
from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import event
from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.generate_so_thu_tu import generate_number
def generate_ma_ho_so():
    so_thu_tu = generate_number("danhmuc_van_bang_chuyen_mon")
    data = "VB" + str(so_thu_tu).zfill(3)
    return data


class VanBangChuyenMon(db.Model):
    __tablename__ = "danhmuc_van_bang_chuyen_mon"

    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    ma_chuyen_mon = db.Column(db.String,nullable=True)
    ten = db.Column(db.String,nullable=True)
    ten_khong_dau = db.Column(db.String,nullable=True)
    trang_thai = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP,server_default= db.func.current_timestamp(),nullable=True)
    updated_at = db.Column(db.TIMESTAMP,server_default= db.func.current_timestamp(),nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    chung_chi_hanh_nghe = db.relationship("ChungChiHanhNghe", back_populates="van_bang_chuyen_mon")

    def __init__(
        self,
        ma_chuyen_mon = None,
        ten = None, 
        trang_thai = None,
    ):
        self.id = uuid.uuid4()
        self.ma_chuyen_mon = generate_ma_ho_so()
        self.ten = ten
        self.ten_khong_dau = clean_string(ten)
        self.trang_thai = trang_thai
        self.ten = ten
@event.listens_for(VanBangChuyenMon, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(VanBangChuyenMon, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()  
       


