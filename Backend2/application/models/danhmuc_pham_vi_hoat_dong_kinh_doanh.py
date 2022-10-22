from datetime import datetime
from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import event
from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.generate_so_thu_tu import generate_number


def generate_ma_ho_so():
    so_thu_tu = generate_number("danhmuc_pham_vi_hoat_dong_kinh_doanh")
    data = "KD" + str(so_thu_tu).zfill(3)
    return data


class PhamViHoatDongKinhDoanh(db.Model):
    __tablename__ = "danhmuc_pham_vi_hoat_dong_kinh_doanh"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ma_hoat_dong_kinh_doanh = db.Column(db.String, nullable=True)
    ten = db.Column(db.String, nullable=True)
    ten_khong_dau = db.Column(db.String, nullable=True)
    chi_tiet = db.Column(db.String, nullable=True)
    loai = db.Column(db.String, nullable=True)
    trang_thai = db.Column(db.Boolean, default=True)
    stt = db.Column(db.String, nullable=True)
    ten_in = db.Column(db.String, nullable=True)
    parent_id = db.Column(UUID(as_uuid=True), db.ForeignKey("danhmuc_pham_vi_hoat_dong_kinh_doanh.id"), nullable=True)

    created_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=True)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    children = db.relationship("PhamViHoatDongKinhDoanh", remote_side=[parent_id], join_depth=1)

    def __init__(
        self,
        ma_hoat_dong_kinh_doanh=None,
        ten=None,
        chi_tiet=None,
        loai=None,
        trang_thai=None,
        stt=None,
        ten_in=None,


    ):
        self.id = uuid.uuid4()
        self.ma_hoat_dong_kinh_doanh = generate_ma_ho_so()
        self.ten = ten
        self.chi_tiet = chi_tiet
        self.loai = loai
        self.ten_khong_dau = clean_string(ten)
        self.ten = ten
        self.trang_thai = trang_thai
        self.stt = stt
        self.ten_in = ten_in


@event.listens_for(PhamViHoatDongKinhDoanh, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(PhamViHoatDongKinhDoanh, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()
