
import datetime
from application.commons.commons import CommonModel
from application.extensions import db
import uuid
from sqlalchemy import event
from sqlalchemy.dialects.postgresql import UUID
from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.generate_so_thu_tu import generate_number

def generate_ma_ho_so():
    so_thu_tu = generate_number("danhmuc_pham_vi_hoat_dong_chuyen_mon")
    data = "PV" + str(so_thu_tu).zfill(3)
    return data

class PhamViHoatDongChuyenMon(CommonModel):
    __tablename__ = "danhmuc_pham_vi_hoat_dong_chuyen_mon"

    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    ma = db.Column(db.String,nullable=True)
    ten = db.Column(db.String,nullable=True)
    ten_khong_dau = db.Column(db.String,nullable=True)
    trang_thai = db.Column(db.Boolean,nullable=True)


    def __init__(
        self,
        ma= None,
        ten = None, 
        trang_thai = None,


    ):
        self.id = uuid.uuid4()
        self.ma= generate_ma_ho_so()
        self.ten = ten
        self.ten_khong_dau = clean_string(ten)
        self.ten = ten
        self.trang_thai = trang_thai
       
@event.listens_for(PhamViHoatDongChuyenMon, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(PhamViHoatDongChuyenMon, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()      


