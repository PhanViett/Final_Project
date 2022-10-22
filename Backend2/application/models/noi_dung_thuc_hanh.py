
from email.policy import default
from application.commons.commons import CommonModel
from application.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid,datetime
from application.utils.helper.string_processing_helper import clean_string
from application.extensions import db, pwd_context
from sqlalchemy import event
from application.utils.helper.generate_so_thu_tu import generate_number


def generate_ma_ho_so():
    so_thu_tu = generate_number("noi_dung_thuc_hanh")
    data = "TH" + str(so_thu_tu).zfill(3)
    return data

class NoiDungThucHanh(CommonModel):

    __tablename__="noi_dung_thuc_hanh"
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    ma_noi_dung_thuc_hanh = db.Column(db.String,nullable=True)
    ten = db.Column(db.String,nullable=True)
    ten_khong_dau = db.Column(db.String,nullable=True)
    trang_thai = db.Column(db.Boolean,nullable=True,default= True)

    def __init__(
        self,
        ma_noi_dung_thuc_hanh=None,
        ten= None,
        trang_thai = None
    ):
        self.id = uuid.uuid4()
        self.ma_noi_dung_thuc_hanh =generate_ma_ho_so()
        self.ten = ten
        self.ten_khong_dau =clean_string(ten)
        self.trang_thai = trang_thai
@event.listens_for(NoiDungThucHanh, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(NoiDungThucHanh, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()