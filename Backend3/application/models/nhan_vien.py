import uuid
import pytz
from typing import cast
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import event, func, Index
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import true
from flask_jwt_extended import current_user
from application.extensions import db, pwd_context
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.dialects.postgresql import JSONB, TEXT
from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.convert_timestamp_helper import get_current_time

lk_vai_tro_nhan_vien = db.Table(
"lk_vai_tro_nhan_vien", db.Model.metadata,
    db.Column("vai_tro_id", UUID(as_uuid=True),  db.ForeignKey('vai_tro.id'), primary_key=True),
    db.Column("user_id", UUID(as_uuid=True),  db.ForeignKey('users.id'), primary_key=True))

class Users(db.Model):
    __tablename__ = "users"

    created_at = db.Column(db.BigInteger, nullable=True)
    updated_at = db.Column(db.BigInteger, nullable=True)
    deactive_at = db.Column(db.BigInteger, nullable=True)
    deleted_at = db.Column(db.BigInteger, nullable=True)

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
    email = db.Column(db.String(80), nullable=True)

    dia_chi = db.Column(db.String, nullable=True)
    so_nha = db.Column(db.String, nullable=True)
    # tinh_thanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tinh_thanh.id"), nullable=True)
    # quan_huyen_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quan_huyen.id"), nullable=True)
    # xa_phuong_id = db.Column(UUID(as_uuid=True), db.ForeignKey("xa_phuong.id"), nullable=True)

    assigned_role = db.relationship("VaiTro", secondary="lk_vai_tro_nhan_vien",
                                    cascade="delete",  lazy="subquery", backref=db.backref("users", lazy=True))    
    tai_khoan_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tai_khoan.id"), nullable=True)
    password = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    vai_tro_id = db.Column(UUID(as_uuid=True), db.ForeignKey("vai_tro.id"), nullable=True)
    
    records = db.relationship("Records", foreign_keys="Records.user_id", back_populates="users", uselist=False)


    def __repr__(self):
        return "<Users %s>" % self.ten

    def __init__(self, tai_khoan_id=None, email=None, active=None, noi_cap=None,
                 ho=None, ten=None, so_nha=None, dia_chi=None, dien_thoai=None, ngay_cap=None,
                 id_mapping=None, so_nha_thuong_tru=None, dia_chi_thuong_tru=None,
                 ma_cong_dan=None, gioi_tinh=None, quan_huyen_id=None, tinh_thanh_id=None, xa_phuong_id=None,
                 quan_huyen_hien_nay_id=None, tinh_thanh_hien_nay_id=None, xa_phuong_hien_nay_id=None, van_bang_chuyen_mon_id=None,
                 noi_tot_nghiep_id=None, nam_tot_nghiep=None, gioithieu=None, avatar_url=None, da_cap_chung_chi=None, vai_tro_id=None,
                 ngay_sinh=None, chuc_vu=None):
        self.id = uuid.uuid4()
        self.tai_khoan_id = tai_khoan_id
        self.email = email
        self.ho = ho
        self.ten = ten
        self.so_nha = so_nha
        self.dia_chi = dia_chi
        self.quan_huyen_hien_nay_id = quan_huyen_hien_nay_id
        self.tinh_thanh_hien_nay_id = tinh_thanh_hien_nay_id
        self.xa_phuong_hien_nay_id = xa_phuong_hien_nay_id
        self.dien_thoai = dien_thoai
        self.active = active
        self.noi_cap = noi_cap
        self.ngay_cap = ngay_cap
        self.ngay_sinh = ngay_sinh
        self.id_mapping = id_mapping
        self.gioi_tinh = gioi_tinh
        self.ma_cong_dan = ma_cong_dan
        self.so_nha_thuong_tru = so_nha_thuong_tru
        self.dia_chi_thuong_tru = dia_chi_thuong_tru
        self.quan_huyen_id = quan_huyen_id
        self.tinh_thanh_id = tinh_thanh_id
        self.xa_phuong_id = xa_phuong_id
        self.van_bang_chuyen_mon_id = van_bang_chuyen_mon_id
        self.noi_tot_nghiep_id = noi_tot_nghiep_id
        self.nam_tot_nghiep = nam_tot_nghiep
        self.gioithieu = gioithieu
        self.avatar_url = avatar_url
        self.da_cap_chung_chi = da_cap_chung_chi
        self.vai_tro_id = vai_tro_id
        self.ho_ten = " ".join(filter(None, [ho, ten]))
        self.ten_khong_dau = clean_string(self.ho_ten)
        self.chuc_vu = chuc_vu

    def __str__(self):
        return "ID=%d, Email=%s, last_name=%s, first_name=%s, address=%s, phone=%s" % \
               (self.id, self.email, self.ho, self.ten, self.dia_chi)

    def create_tsvector(*args):
        exp = args[0]
        for e in args[1:]:
            exp += ' ' + e
        return func.to_tsvector('english', exp)

    __ts_vector__ = create_tsvector(
        cast(func.coalesce(ten, ''), TEXT)
    )

    __table_args__ = (
        Index(
            'idx_user_fts',
            __ts_vector__,
            postgresql_using='gin'
        ),
    )

# TRIGGERS


@ event.listens_for(Users, "before_insert")
def on_update_trigger(mapper, connection, target: Users):
    target.created_at = get_current_time("int")
    target.updated_at = get_current_time("int")
    target.created_by = current_user.id if current_user else None


@ event.listens_for(Users, "before_update")
def on_update_trigger(mapper, connection, target: Users):
    target.updated_at = get_current_time("int")
    target.ho_ten = " ".join(filter(None, [target.ho, target.ten]))
    target.ten_khong_dau = clean_string(target.ho_ten)
