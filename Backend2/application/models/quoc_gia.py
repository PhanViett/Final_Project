
from sqlalchemy.dialects.postgresql import UUID
import uuid
from application.extensions import db
from application.commons.commons import CommonModel


class QuocGia(db.Model):

    __tablename__="quoc_gia"
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    ten = db.Column(db.String, nullable=True)
    tenkhongdau = db.Column(db.String,nullable=True)
    ma = db.Column(db.String,nullable=True)
    trang_thai = db.Column(db.String,nullable=True)
    loai = db.Column(db.String, nullable=True)
    active = db.Column(db.String, nullable=True)
    created_at = db.Column(db.String, nullable=True)
    created_by = db.Column(db.String, nullable=True)
    updated_at = db.Column(db.String, nullable=True)
    updated_by = db.Column(db.String, nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String, nullable=True)
    deleted_at = db.Column(db.String, nullable=True)


    def __init__(self) -> None:
        return self

