
from datetime import datetime
from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.mutable import MutableDict
from application.commons.commons import CommonModel


class ThongBao(CommonModel):
    __tablename__ = "thong_bao"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tieu_de = db.Column(db.String, nullable=True)
    noi_dung = db.Column(db.String, nullable=True)
    loai = db.Column(db.Integer, nullable=True)
    trang_thai = db.Column(db.Boolean, default=True)
    nhan_vien_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"), nullable=True)
    notify_at = db.Column(db.BigInteger, nullable=True)
    read_at = db.Column(db.BigInteger, nullable=True)
    dinh_kem = db.Column(MutableDict.as_mutable(JSONB), nullable=True)
    nhan_vien = db.relationship("User", foreign_keys=[nhan_vien_id], back_populates="thong_bao", uselist=False)

    def __init__(
        self,
        tieu_de=None,
        noi_dung=None,
        loai=None,
        trang_thai=None,
        nhan_vien_id=None,
        notify_at=None,
        dinh_kem={}
    ):
        self.id = uuid.uuid4()
        self.tieu_de = tieu_de
        self.noi_dung = noi_dung
        self.loai = loai
        self.trang_thai = trang_thai
        self.nhan_vien_id = nhan_vien_id
        self.notify_at = notify_at if notify_at else int(datetime.now().timestamp())
        self.dinh_kem = dinh_kem
