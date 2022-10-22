
import datetime
from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

from application.utils.helper.string_processing_helper import clean_string
from sqlalchemy import event
from application.utils.helper.generate_so_thu_tu import generate_number

def generate_ma_ho_so():
    so_thu_tu = generate_number("danh_muc_hoi_dong")
    data = "HD" + str(so_thu_tu).zfill(3)
    return data
class HoiDong(db.Model):
    __tablename__ = "danhmuc_hoi_dong"

    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4())
    ma_hoi_dong = db.Column(db.String,nullable=True)
    ten_hoi_dong = db.Column(db.String,nullable=True)
    ten_khong_dau = db.Column(db.String,nullable=True)
    ngay_thanh_lap = db.Column(db.String, nullable= True)
    ten_nguoi_phu_trach = db.Column(db.String,nullable=True)
    trang_thai = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP,server_default= db.func.current_timestamp(),nullable=True)
    updated_at = db.Column(db.TIMESTAMP,server_default= db.func.current_timestamp(),nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)


    def __init__(
        self,
        ma_hoi_dong = None,
        ten_hoi_dong= None,  
        ngay_thanh_lap =None,
        ten_nguoi_phu_trach=None,
        trang_thai = None,


    ):
        self.id = uuid.uuid4()
        self.ma_hoi_dong = generate_ma_ho_so()
        self.ten_hoi_dong = ten_hoi_dong
        self.ten_khong_dau = clean_string(ten_hoi_dong)
        self.ngay_thanh_lap = ngay_thanh_lap
        self.ten_nguoi_phu_trach = ten_nguoi_phu_trach       
        self.trang_thai = trang_thai
   

@event.listens_for(HoiDong, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(HoiDong, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()
