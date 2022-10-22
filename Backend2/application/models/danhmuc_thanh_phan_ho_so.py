
import datetime
from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import event
from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.generate_so_thu_tu import generate_number
def generate_ma_ho_so():
    so_thu_tu = generate_number("danhmuc_thanh_phan_ho_so")
    data = "TP" + str(so_thu_tu).zfill(3)
    return data

class ThanhPhanHoSo(db.Model):
    __tablename__ = "danhmuc_thanh_phan_ho_so"

    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    ma_tp_ho_so = db.Column(db.String,nullable=True)
    ten = db.Column(db.String,nullable=True)
    ten_khong_dau = db.Column(db.String,nullable=True)
    thu_tuc_id = db.Column(UUID(as_uuid=True), db.ForeignKey("danhmuc_thu_tuc.id"), nullable=True)
    trang_thai = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP,server_default= db.func.current_timestamp(),nullable=True)
    updated_at = db.Column(db.TIMESTAMP,server_default= db.func.current_timestamp(),nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)


    thu_tuc = db.relationship("DanhMucThuTuc",lazy="joined", back_populates="ho_so")
    

    def __init__(
        self,
        ma_tp_ho_so = None,
        ten = None, 
        thu_tuc_id = None,
        trang_thai = None,


    ):
        self.id = uuid.uuid4()
        self.ma_tp_ho_so = generate_ma_ho_so()
        self.ten = ten
        self.ten_khong_dau = clean_string(ten)
        self.thu_tuc_id = thu_tuc_id
        self.trang_thai = trang_thai
@event.listens_for(ThanhPhanHoSo, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(ThanhPhanHoSo, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()         
       


