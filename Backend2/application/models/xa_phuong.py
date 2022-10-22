
from sqlalchemy.dialects.postgresql import UUID
import uuid
from application.extensions import db
from application.commons.commons import CommonModel


class XaPhuong(db.Model):

    __tablename__="xa_phuong"
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    ten = db.Column(db.String, nullable=True)
    tenkhongdau = db.Column(db.String,nullable=True)
    ma = db.Column(db.String,nullable=True)
    trang_thai = db.Column(db.String,nullable=True)
    loai = db.Column(db.String, nullable=True)
    quanhuyen_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quan_huyen.id"), nullable=True)
    tinhthanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tinh_thanh.id"), nullable=True)
    active = db.Column(db.String, nullable=True)
    created_at = db.Column(db.String, nullable=True)
    created_by = db.Column(db.String, nullable=True)
    updated_at = db.Column(db.String, nullable=True)
    updated_by = db.Column(db.String, nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String, nullable=True)
    deleted_at = db.Column(db.String, nullable=True)
    

    quanhuyen = db.relationship("QuanHuyen", foreign_keys=[quanhuyen_id],lazy="joined", uselist=False)
    tinhthanh = db.relationship("TinhThanh", foreign_keys=[tinhthanh_id],lazy="joined", uselist=False)

    def __init__(self) -> None:
        return self

