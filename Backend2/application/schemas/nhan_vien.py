from enum import unique
import re
from flask import json
from marshmallow_sqlalchemy.schema import auto_field
from application.models import User
from application.extensions import ma, db

from marshmallow import ValidationError, fields, missing, validates
from application.schemas.bang_cap import BangCapNguoiHanhNgheSchema
from application.schemas.vai_tro import VaiTroDisplaySchema, VaiTroSchema

from application.utils.validate.uuid_validator import is_valid_uuid


class NhanVienSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    # is_super_admin = ma.auto_field(load_only=True)
    # vai_tro_id = ma.auto_field()
    assigned_role = ma.Nested(VaiTroSchema, many=True)
    last_login = fields.DateTime(format="%H:%M:%S %d/%m/%Y",
                                 attribute="tai_khoan.last_login_at", dump_only=True, default=None)
    ngay_cap = ma.auto_field()
    ngay_sinh = ma.auto_field()
    quan_huyen_hien_nay_id = ma.auto_field()
    quan_huyen_id = ma.auto_field()
    tinh_thanh_hien_nay_id = ma.auto_field()
    tinh_thanh_id = ma.auto_field()
    xa_phuong_hien_nay_id = ma.auto_field()
    xa_phuong_id = ma.auto_field()

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")

# ONLY FOR SHOW


class NhanVienWithRoleSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    mat_khau = ma.String(load_only=True, required=True)
    email = fields.Email()
    vai_tro_id = ma.String(load_only=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")


class NhanVienHanhNgheSchema(ma.SQLAlchemySchema):
    id = ma.auto_field(dump_only=True)
    ho_ten = fields.String(attribute="ho_ten", dump_only=True)
    ngay_sinh = fields.Integer(attribute="ngay_sinh", dump_only=True)
    gioi_tinh = fields.String(attribute="gioi_tinh", dump_only=True)
    email = fields.String(attribute="email", dump_only=True)
    dien_thoai = fields.String(attribute="dien_thoai", dump_only=True)
    cmnd = fields.String(attribute="ma_cong_dan", dump_only=True)
    ngay_cap_cmnd = fields.Integer(attribute="ngay_cap", dump_only=True)
    noi_cap_cmnd = fields.String(attribute="noi_cap", dump_only=True)
    ho_khau_thuong_tru = fields.Method("get_ho_khau_thuong_tru")
    ho_khau_hien_tai = fields.Method("get_ho_khau_hien_nay")

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True

    def get_ho_khau_thuong_tru(self, obj: User):
        if obj:
            dia_chi_thuong_tru = obj.dia_chi_thuong_tru
            ten_phuong_xa = obj.xa_phuong.ten if obj.xa_phuong else None
            ten_quan_huyen = obj.quan_huyen.ten if obj.quan_huyen else None
            ten_tinh_thanh = obj.tinh_thanh.ten if obj.tinh_thanh else None
            return ", ".join(filter(None, [dia_chi_thuong_tru, ten_phuong_xa, ten_quan_huyen, ten_tinh_thanh]))
        return None

    def get_ho_khau_hien_nay(self, obj: User):
        if obj:
            dia_chi = obj.dia_chi
            ten_phuong_xa = obj.xa_phuong_hien_nay.ten if obj.xa_phuong else None
            ten_quan_huyen = obj.quan_huyen_hien_nay.ten if obj.quan_huyen else None
            ten_tinh_thanh = obj.tinh_thanh_hien_nay.ten if obj.tinh_thanh else None
            return ", ".join(filter(None, [dia_chi, ten_phuong_xa, ten_quan_huyen, ten_tinh_thanh]))
        return None


class NhanVienWithTaiKhoanSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    email = fields.Email()
    tai_khoan_id = ma.auto_field(load_only=True)
    ten_tai_khoan = fields.String(attribute="assigned_account.tai_khoan", dump_only=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")


class QuanLyNguoiDungSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    tai_khoan_id = ma.auto_field(load_only=True)
    quan_huyen_id = ma.auto_field()
    tinh_thanh_id = ma.auto_field()
    xa_phuong_id = ma.auto_field()
    van_bang_chuyen_mon_id = ma.auto_field()
    noi_tot_nghiep_id = ma.auto_field()
    vai_tro_id = ma.auto_field()
    quan_huyen_hien_nay_id = ma.auto_field()
    tinh_thanh_hien_nay_id = ma.auto_field()
    xa_phuong_hien_nay_id = ma.auto_field()

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at", "id_mapping")


class NguoiDungDisplaySchema(ma.SQLAlchemySchema):
    id = fields.String(dump_only=True)
    ho_ten = fields.String(dump_only=True)
    active = fields.Boolean(dump_only=True)
    tai_khoan = fields.String(attribute="tai_khoan.tai_khoan", allow_none=True, dump_default=None, dump_only=True)
    email = fields.String(dump_only=True)
    ho = fields.String(dump_only=True)
    ten = fields.String(dump_only=True)
    ngay_sinh = fields.String(dump_only=True)
    gioi_tinh = fields.String(dump_only=True)
    gioithieu = fields.String(dump_only=True)
    avatar_url = fields.String(dump_only=True)
    display_chuc_vu = fields.Boolean(dump_only=True)
    da_cap_chung_chi = fields.String(dump_only=True)
    dien_thoai = fields.String(dump_only=True)
    quan_huyen_id = fields.String(dump_only=True)
    tinh_thanh_id = fields.String(dump_only=True)
    xa_phuong_id = fields.String(dump_only=True)
    # ho khau thuong tru
    # tinh_thanh_hien_nay = fields.Str(attribute="tinh_thanh.ten",allow_none=True,dump_default=None)
    # xa_phuong_hien_nay =  fields.Str(attribute="xa_phuong.ten",allow_none=True,dump_default=None)
    # quan_huyen_hien_nay =  fields.Str(attribute="quan_huyen.ten",allow_none=True,dump_default=None)
    #  cho o hien nay
    quan_huyen_hien_nay_id = fields.String(dump_only=True)
    tinh_thanh_hien_nay_id = fields.String(dump_only=True)
    xa_phuong_hien_nay_id = fields.String(dump_only=True)
    dia_chi_thuong_tru = fields.String(dump_only=True)
    dia_chi = fields.String(dump_only=True)
    ma_cong_dan = fields.String(dump_only=True)
    ngay_cap = fields.String(dump_only=True)
    noi_cap = fields.String(dump_only=True)
    van_bang_chuyen_mon_id = fields.String(dump_only=True)
    noi_tot_nghiep_id = fields.String(dump_only=True)
    nam_tot_nghiep = fields.String(dump_only=True)
    ten_khong_dau = fields.String(dump_only=True)
    chuc_vu = fields.String(dump_only=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True


class ThongTinHanhChinhSchema(ma.SQLAlchemySchema):
    id = fields.String(dump_only=True)
    ho_ten = fields.String(allow_none=True)
    email = fields.String(allow_none=True)
    ngay_sinh = fields.Integer(allow_none=True)
    gioi_tinh = fields.String(allow_none=True)
    dien_thoai = fields.String(allow_none=True)

    so_nha = fields.String(allow_none=True)
    xa_phuong_hien_nay_id = fields.String(allow_none=True)
    quan_huyen_hien_nay_id = fields.String(allow_none=True)
    tinh_thanh_hien_nay_id = fields.String(allow_none=True)

    so_nha_thuong_tru = fields.String(allow_none=True)
    xa_phuong_id = fields.String(allow_none=True)
    quan_huyen_id = fields.String(allow_none=True)
    tinh_thanh_id = fields.String(allow_none=True)

    ma_cong_dan = fields.String(allow_none=True)
    ngay_cap = fields.Integer(allow_none=True)
    noi_cap = fields.String(allow_none=True)
    noi_tot_nghiep_id = ma.auto_field(load_only=True, allow_none=True)
    noi_tot_nghiep = fields.String(attribute="noi_tot_nghiep.ten", dump_only=True)
    nam_tot_nghiep = fields.String(allow_none=True)
    ten_khong_dau = fields.String(allow_none=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
