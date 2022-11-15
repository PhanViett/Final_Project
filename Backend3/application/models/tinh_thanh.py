
from sqlalchemy.dialects.postgresql import UUID, SMALLINT
import uuid
from application.extensions import db
from application.utils.helper.string_processing_helper import clean_string


class TinhThanh(db.Model):

    __tablename__ = "tinh_thanh"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ten = db.Column(db.String, nullable=True)
    tenkhongdau = db.Column(db.String, nullable=True)
    ma = db.Column(db.String, nullable=True)
    trang_thai = db.Column(db.String, nullable=True)
    loai = db.Column(SMALLINT, nullable=True)
    active = db.Column(db.String, nullable=True)
    created_at = db.Column(db.String, nullable=True)
    created_by = db.Column(db.String, nullable=True)
    updated_at = db.Column(db.String, nullable=True)
    updated_by = db.Column(db.String, nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String, nullable=True)
    deleted_at = db.Column(db.String, nullable=True)

    def __init__(self, ten, loai) -> None:
        self.ten = ten
        self.loai = loai
        self.tenkhongdau = clean_string(ten)
