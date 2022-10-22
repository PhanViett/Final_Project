
from application.commons.commons import CommonModel
from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

from application.utils.helper.string_processing_helper import clean_string


class LOAIMAGPS(CommonModel):
    __tablename__ = "loai_magps"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ma_gps = db.Column(db.String, nullable=True)
    ten = db.Column(db.String, nullable=True)
    ten_khong_dau = db.Column(db.String, nullable=True)
    trang_thai = db.Column(db.Boolean, default=True)
    so_da_cap = db.Column(db.Integer, default=True)

    def __init__(
        self,
        ma_gps=None,
        ten=None,
        trang_thai=None,
        so_da_cap=None
    ):
        self.id = uuid.uuid4()
        self.ma_gps = ma_gps
        self.ten = ten
        self.ten_khong_dau = clean_string(ten)
        self.so_da_cap = so_da_cap
        self.trang_thai = trang_thai
