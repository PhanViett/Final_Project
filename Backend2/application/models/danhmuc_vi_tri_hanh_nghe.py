from datetime import datetime
from enum import unique
from application.extensions import db
import uuid
from sqlalchemy import event
from sqlalchemy.dialects.postgresql import UUID
from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.generate_so_thu_tu import generate_number


def generate_ma_ho_so():
    so_thu_tu = generate_number("danhmuc_vi_tri_hanh_nghe")
    data = "HN" + str(so_thu_tu).zfill(3)
    return data


class ViTriHanhNghe(db.Model):
    __tablename__ = "danhmuc_vi_tri_hanh_nghe"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ma_hanh_nghe = db.Column(db.String, nullable=True)
    ten = db.Column(db.String, nullable=True)
    rut_gon = db.Column(db.String, nullable=True)
    ten_khong_dau = db.Column(db.String, nullable=True)
    loai = db.Column(db.String, nullable=True)
    parent_id = db.Column(UUID(as_uuid=True), db.ForeignKey("danhmuc_vi_tri_hanh_nghe.id"), nullable=True)
    trang_thai = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=True)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    children = db.relationship("ViTriHanhNghe", remote_side=[parent_id], join_depth=1)

    def __init__(
        self,
        ma_hanh_nghe=None,
        ten=None,
        rut_gon=None,
        loai=None,
        parent_id=None,
        trang_thai=None,
    ):
        self.id = uuid.uuid4()
        self.ma_hanh_nghe = generate_ma_ho_so()
        self.ten = ten
        self.ten_khong_dau = clean_string(ten)
        self.loai = loai
        self.rut_gon = rut_gon
        self.parent_id = parent_id
        self.loai = loai
        self.trang_thai = trang_thai


@event.listens_for(ViTriHanhNghe, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(ViTriHanhNghe, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()
