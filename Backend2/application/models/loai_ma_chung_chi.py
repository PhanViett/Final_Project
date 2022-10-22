
from application.commons.commons import CommonModel
from application.extensions import db
import uuid, datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import event

from application.utils.helper.string_processing_helper import clean_string



class LOAIMACHUNGCHI(CommonModel):
    __tablename__ = "loai_ma_chung_chi"
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    ma_chung_chi = db.Column(db.String,nullable=True)
    ten = db.Column(db.String,nullable=True)
    ten_khong_dau = db.Column(db.String,nullable=True)
    trang_thai = db.Column(db.String,nullable=True)
    so_da_cap = db.Column(db.BigInteger)
    mac_dinh = db.Column(db.Boolean)
    doi_tuong = db.Column(db.Integer)

    def __init__(
        self,
        ma_chung_chi=None,
        ten= None,
        trang_thai = None,
        so_da_cap =None,
        doi_tuong = None,
        mac_dinh = None
    ):
        self.id = uuid.uuid4()
        self.ma_chung_chi =ma_chung_chi
        self.ten = ten
        self.ten_khong_dau =clean_string(ten)
        self.so_da_cap =so_da_cap
        self.doi_tuong = doi_tuong
        self.trang_thai = trang_thai
        self.mac_dinh = mac_dinh
@event.listens_for(LOAIMACHUNGCHI, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(LOAIMACHUNGCHI, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()
       
       


