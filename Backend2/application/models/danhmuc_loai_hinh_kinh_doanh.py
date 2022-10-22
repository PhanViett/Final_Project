
import datetime

from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import event

from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.generate_so_thu_tu import generate_number

def generate_ma_ho_so():
    so_thu_tu = generate_number("danh_muc_loai_hinh_kinh_doanh")
    data = "LH" + str(so_thu_tu).zfill(3)
    return data

class LoaiHinhKinhDoanh(db.Model):
    __tablename__ = "danhmuc_loai_hinh_kinh_doanh"

    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    ma_loai_hinh = db.Column(db.String,nullable=True)
    ten = db.Column(db.String,nullable=True)
    ten_khong_dau = db.Column(db.String,nullable=True)
    trang_thai = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP,server_default= db.func.current_timestamp(),nullable=True)
    updated_at = db.Column(db.TIMESTAMP,server_default= db.func.current_timestamp(),nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)


    def __init__(
        self,
        ma_loai_hinh = None,
        ten= None,
        trang_thai = None,


    ):
        self.id = uuid.uuid4()
        self.ma_loai_hinh = generate_ma_ho_so()
        self.ten = ten
        self.ten_khong_dau =clean_string(ten)
        
        
        self.trang_thai = trang_thai
       
        # self.is_super_admin = is_super_admin
       

@event.listens_for(LoaiHinhKinhDoanh, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(LoaiHinhKinhDoanh, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()
