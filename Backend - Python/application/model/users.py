import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from application.extensions import db, pwd_context
from application.utils.helper.string_processing_helper import clean_string


class User(db.Model):
    __tablename__ = 'users'
    created_at = db.Column(db.BigInteger, default=int(datetime.utcnow().timestamp()), nullable=True)
    updated_at = db.Column(db.BigInteger, default=int(datetime.utcnow().timestamp()), nullable=True)
    deactive_at = db.Column(db.BigInteger, nullable=True)
    delete_at = db.Column(db.BigInteger, nullable=True)

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tai_khoan_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tai_khoan.id"), nullable=True)
    ho = db.Column(db.String(80), nullable=True)
    ten = db.Column(db.String(80), nullable=True)
    ho_ten = db.Column(db.String(80), nullable=True)
    ten_khong_dau = db.Column(db.String(80), nullable=True)
    avatar_url = db.Column(db.String, nullable=True)
    ngay_sinh = db.Column(db.BigInteger, nullable=True)
    gioi_tinh = db.Column(db.String, nullable=True)
    dien_thoai = db.Column(db.String(12), nullable=True)
    ma_cong_dan = db.Column(db.String(80), nullable=True)
    ngay_cap = db.Column(db.BigInteger, nullable=True)
    noi_cap = db.Column(db.String(80), nullable=True)

    dia_chi = db.Column(db.String, nullable=True)
    so_nha = db.Column(db.String, nullable=True)
    tinh_thanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tinh_thanh.id"), nullable=True)
    quan_huyen_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quan_huyen.id"), nullable=True)
    xa_phuong_id = db.Column(UUID(as_uuid=True), db.ForeignKey("xa_phuong.id"), nullable=True)

    assigned_role = db.relationship("VaiTro", secondary="lk_vai_tro_nhan_vien",
                                    cascade="delete",  lazy="subquery", backref=db.backref("nhan_vien", lazy=True))
    vai_tro = db.Column(db.String, nullable=False)
    tai_khoan = db.Column(db.String, nullable=True)
    password_hash = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)

def __init__(self, tai_khoan=None, password_hash=None, ho=None, ten=None, avatar_url=None, ngay_sinh=None, gioi_tinh=None, dien_thoai=None, ma_cong_dan=None, email=None, active=None,
                ngay_cap=None, noi_cap=None, dia_chi=None, so_nha=None, tinh_thanh_id=None, quan_huyen_id=None, xa_phuong_id=None, vai_tro=None):
    self.id = uuid.uuid4()
    self.tai_khoan = tai_khoan
    self.password_hash = pwd_context.hash(password_hash)
    self.ho = ho
    self.ten = ten
    self.ho_ten = " ".join(filter(None, [ho, ten]))
    self.ten_khong_dau = clean_string(self.ho_ten)
    self.avatar_url = avatar_url
    self.ngay_sinh = ngay_sinh
    self.gioi_tinh = gioi_tinh
    self.dien_thoai = dien_thoai
    self.ma_cong_dan = ma_cong_dan
    self.email = email
    self.ngay_cap = ngay_cap
    self.noi_cap = noi_cap

    self.dia_chi = dia_chi
    self.so_nha = so_nha
    self.tinh_thanh_id = tinh_thanh_id
    self.quan_huyen_id = quan_huyen_id
    self.xa_phuong_id = xa_phuong_id

    self.vai_tro = vai_tro
    self.active = active