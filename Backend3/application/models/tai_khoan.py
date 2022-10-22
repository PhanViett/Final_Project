import uuid
from sqlalchemy import event
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from application.extensions import db, pwd_context
from application.utils.helper.convert_timestamp_helper import get_current_time


class TaiKhoan(db.Model):
    __tablename__ = "tai_khoan"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tai_khoan = db.Column(db.String(), nullable=False, unique=True)
    mat_khau = db.Column(db.String(), nullable=False)
    dien_thoai = db.Column(db.String(12), nullable=True)
    type = db.Column(db.SmallInteger, nullable=True, default=0)  # ! 0 : User ; 1 : Co So
    last_login_at = db.Column(db.TIMESTAMP, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=True)
    updated_at = db.Column(db.BigInteger, nullable=True)

    def __init__(self, tai_khoan=None, mat_khau=None, dien_thoai=None, type=None) -> None:
        self.id = uuid.uuid4()
        self.tai_khoan = tai_khoan
        self.mat_khau = pwd_context.hash(mat_khau)
        self.dien_thoai = dien_thoai
        self.type = type
        self.created_at = get_current_time("int")
        self.updated_at = get_current_time("int")

@ event.listens_for(TaiKhoan, "before_insert")
def on_update_trigger(mapper, connection, target: TaiKhoan):
    target.created_at = get_current_time("int")
    target.updated_at = get_current_time("int")


@event.listens_for(TaiKhoan, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = get_current_time("int")