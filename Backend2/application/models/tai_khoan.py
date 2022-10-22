from datetime import datetime
import uuid
from application.extensions import db, pwd_context
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import event


class TaiKhoan(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tai_khoan = db.Column(db.String(), nullable=False, unique=True)
    mat_khau = db.Column(db.String(), nullable=False)
    dien_thoai = db.Column(db.String(12), nullable=True)
    type = db.Column(db.SmallInteger, nullable=True, default=0)  # ! 0 : User ; 1 : Co So
    last_login_at = db.Column(db.TIMESTAMP, nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=True)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=True)

    def __init__(self, tai_khoan=None, mat_khau=None, dien_thoai=None, type=None) -> None:
        self.id = uuid.uuid4()
        self.tai_khoan = tai_khoan
        self.mat_khau = pwd_context.hash(mat_khau)
        self.dien_thoai = dien_thoai
        self.type = type
        self.created_at = datetime.now()
        self.updated_at = self.created_at


@event.listens_for(TaiKhoan, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.now()
