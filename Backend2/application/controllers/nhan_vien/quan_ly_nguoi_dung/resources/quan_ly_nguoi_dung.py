
from datetime import datetime
from functools import partial
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError
from application.commons.pagination import paginate
from application.models import tai_khoan
from application.models import vai_tro
from application.models.quan_huyen import QuanHuyen
from application.models.tai_khoan import TaiKhoan
from application.models.tinh_thanh import TinhThanh
from application.models.user import User
from application.models.vai_tro import VaiTro
from application.models.xa_phuong import XaPhuong
from application.schemas.nhan_vien import NguoiDungDisplaySchema, QuanLyNguoiDungSchema, NhanVienWithRoleSchema, QuanLyNguoiDungSchema
from application.utils.helper.convert_timestamp_helper import convert_timestamp
from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
from application.extensions import db
from application.utils.validate.uuid_validator import is_valid_uuid
from application.extensions import db, pwd_context
from sqlalchemy import and_, or_, not_


class QuanLyThongTinNguoiDungResource(Resource):
    @jwt_required()
    def post(self):

        schema = QuanLyNguoiDungSchema()

        req = {

            "email": request.form.get("email"),
            "ho": request.form.get("ho"),
            "ten": request.form.get("ten"),
            "ngay_sinh": request.form.get("ngay_sinh"),
            "gioi_tinh": request.form.get("gioi_tinh"),
            "gioithieu": request.form.get("gioithieu"),
            "avatar_url": request.form.get("avatar_url"),
            "da_cap_chung_chi": request.form.get("da_cap_chung_chi"),
            "dien_thoai": request.form.get("dien_thoai"),
            "active": request.form.get("active"),
            "quan_huyen_id": request.form.get("quan_huyen_id"),
            "tinh_thanh_id": request.form.get("tinh_thanh_id"),
            "xa_phuong_id": request.form.get("xa_phuong_id"),
            "quan_huyen_hien_nay_id": request.form.get("quan_huyen_hien_nay_id"),
            "tinh_thanh_hien_nay_id": request.form.get("tinh_thanh_hien_nay_id"),
            "xa_phuong_hien_nay_id": request.form.get("xa_phuong_hien_nay_id"),
            "dia_chi_thuong_tru": request.form.get("dia_chi_thuong_tru"),
            "dia_chi": request.form.get("dia_chi"),
            "ma_cong_dan": request.form.get("ma_cong_dan"),
            "ngay_cap": request.form.get("ngay_cap"),
            "noi_cap": request.form.get("noi_cap"),
            "van_bang_chuyen_mon_id": request.form.get("van_bang_chuyen_mon_id"),
            "noi_tot_nghiep_id": request.form.get("noi_tot_nghiep_id"),
            "nam_tot_nghiep": request.form.get("nam_tot_nghiep"),
        }
        try:
            quan_ly_nguoi_dung: User = schema.load(req)
            target_xa_phuong: XaPhuong = XaPhuong.query.filter_by(id=req["xa_phuong_id"]).first()
            if not target_xa_phuong:
                return {
                    "msg": "xã phường không tồn tại!"
                }, HttpCode.BadRequest
            if not str(target_xa_phuong.quanhuyen_id) == req["quan_huyen_id"]:
                return {
                    "msg": "quận huyện không tồn tại!"
                }, HttpCode.BadRequest
            if not str(target_xa_phuong.tinhthanh_id) == req["tinh_thanh_id"]:
                return {
                    "msg": "xã phường không tồn tại!"
                }, HttpCode.BadRequest

            quan_ly_nguoi_dung.dia_chi = ", ".join(filter(
                None, (quan_ly_nguoi_dung.dia_chi, target_xa_phuong.ten, target_xa_phuong.quanhuyen.ten, target_xa_phuong.tinhthanh.ten)))

            target_xa_phuong_hien_nay: XaPhuong = XaPhuong.query.filter_by(id=req["xa_phuong_hien_nay_id"]).first()
            if not target_xa_phuong_hien_nay:
                return {
                    "msg": "xã phường không tồn tại!"
                }, HttpCode.BadRequest
            if not str(target_xa_phuong_hien_nay.quanhuyen_id) == req["quan_huyen_hien_nay_id"]:
                return {
                    "msg": "quận huyện không tồn tại!"
                }, HttpCode.BadRequest
            if not str(target_xa_phuong_hien_nay.tinhthanh_id) == req["tinh_thanh_hien_nay_id"]:
                return {
                    "msg": "xã phường không tồn tại!"
                }, HttpCode.BadRequest

            quan_ly_nguoi_dung.dia_chi_thuong_tru = ", ".join(filter(
                None, (quan_ly_nguoi_dung.dia_chi_thuong_tru, target_xa_phuong_hien_nay.ten, target_xa_phuong_hien_nay.quanhuyen.ten, target_xa_phuong_hien_nay.tinhthanh.ten)))

            # quan_ly_nguoi_dung.tai_khoan_id = current_user.id
            avatar_url = request.files.get("avatar_url")
            if avatar_url is not None:
                try:
                    avatar_url = UploadMinio.upload_duocsi(avatar_url)
                    quan_ly_nguoi_dung.avatar_url = avatar_url
                except:
                    return {"errors": "Tải file thất bại"},  HttpCode.InternalError

            check_tai_khoan = TaiKhoan.query.filter(TaiKhoan.tai_khoan.like(
                f"%{quan_ly_nguoi_dung.ten_khong_dau}%")).all()
            if len(check_tai_khoan) > 0:
                stt = len(check_tai_khoan) + 1
                tai_khoan_duoc_si = quan_ly_nguoi_dung.ten_khong_dau + str(stt)
            else:
                tai_khoan_duoc_si = quan_ly_nguoi_dung.ten_khong_dau
            mat_khau = "12345678"
            tai_khoan = TaiKhoan(tai_khoan=tai_khoan_duoc_si, mat_khau=mat_khau)

            db.session.add(tai_khoan)
            db.session.commit()
            quan_ly_nguoi_dung.tai_khoan_id = tai_khoan.id
            db.session.add(quan_ly_nguoi_dung)
            db.session.commit()

        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest

        return {"msg": "Tạo  quản lý người dùng thành công!!", "results": schema.dump(quan_ly_nguoi_dung)}, HttpCode.Created


class QuanLyNguoiDungById(Resource):
    @jwt_required()
    def put(self, id):
        schema = QuanLyNguoiDungSchema(partial=True)
        quan_ly_nguoi_dung: User = User.query.filter(User.id == id).first()
        if quan_ly_nguoi_dung is None:
            return {"errors": "No data"},  HttpCode.InternalError
        if not is_valid_uuid(id):
            return {
                "errorCode": "EC05",
                "msg": "ID sai định dạng (không phải UUID)"
            }
        req = {
            "email": request.form.get("email"),
            "ho": request.form.get("ho"),
            "ten": request.form.get("ten"),
            "ngay_sinh": request.form.get("ngay_sinh"),
            "gioi_tinh": request.form.get("gioi_tinh"),
            "gioithieu": request.form.get("gioithieu"),
            "avatar_url": request.form.get("avatar_url"),
            # "da_cap_chung_chi": request.form.get("da_cap_chung_chi"),
            "dien_thoai": request.form.get("dien_thoai"),
            "active": request.form.get("active"),
            "quan_huyen_id": request.form.get("quan_huyen_id"),
            "tinh_thanh_id": request.form.get("tinh_thanh_id"),
            "xa_phuong_id": request.form.get("xa_phuong_id"),
            "quan_huyen_hien_nay_id": request.form.get("quan_huyen_hien_nay_id"),
            "tinh_thanh_hien_nay_id": request.form.get("tinh_thanh_hien_nay_id"),
            "xa_phuong_hien_nay_id": request.form.get("xa_phuong_hien_nay_id"),
            "so_nha": request.form.get("so_nha"),
            "so_nha_thuong_tru": request.form.get("so_nha_thuong_tru"),
            # "dia_chi": request.form.get("dia_chi"),
            # "dia_chi_thuong_tru": request.form.get("dia_chi_thuong_tru"),
            "ma_cong_dan": request.form.get("ma_cong_dan"),
            "ngay_cap": request.form.get("ngay_cap"),
            "noi_cap": request.form.get("noi_cap"),
            "van_bang_chuyen_mon_id": request.form.get("van_bang_chuyen_mon_id"),
            "noi_tot_nghiep_id": request.form.get("noi_tot_nghiep_id"),
            "nam_tot_nghiep": request.form.get("nam_tot_nghiep"),
            "ho_ten": request.form.get("ho_ten"),

        }
        # ten = request.form.get('ten')
        # ho = request.form.get('ho')

        # ho_ten = ho +" "+ ten
        # if ten is not None:
        #     quan_ly_nguoi_dung.ten_khong_dau = clean_string(ho_ten)

        try:
            quan_ly_nguoi_dung = schema.load(req, instance=quan_ly_nguoi_dung)
            ten = request.form.get('ten')
            ho = request.form.get('ho')
            ho_ten = ho+" " + ten
            if ten is not None:
                quan_ly_nguoi_dung.ten_khong_dau = clean_string(ho_ten)
            quan_ly_nguoi_dung.ho_ten = ho_ten
            quan_ly_nguoi_dung.created_by = current_user.id

            # dia chi thuong tru
            so_nha_thuong_tru = request.form.get("so_nha_thuong_tru")
            quan_huyen_id = request.form.get("quan_huyen_id")
            xa_phuong_id = request.form.get("xa_phuong_id")
            tinh_thanh_id = request.form.get("tinh_thanh_id")
            quan_huyen_query = QuanHuyen.query.filter(QuanHuyen.id == quan_huyen_id).first()
            xa_phuong_query = XaPhuong.query.filter(XaPhuong.id == xa_phuong_id).first()
            tinh_thanh_query = TinhThanh.query.filter(TinhThanh.id == tinh_thanh_id).first()
            # cho o hien nay
            so_nha = request.form.get("so_nha")
            quan_huyen_hien_nay_id = request.form.get("quan_huyen_hien_nay_id")
            xa_phuong_hien_nay_id = request.form.get("xa_phuong_hien_nay_id")
            tinh_thanh_hien_nay_id = request.form.get("tinh_thanh_hien_nay_id")
            quan_huyen_hien_nay_query = QuanHuyen.query.filter(QuanHuyen.id == quan_huyen_hien_nay_id).first()
            xa_phuong_hien_nay_query = XaPhuong.query.filter(XaPhuong.id == xa_phuong_hien_nay_id).first()
            tinh_thanh_hien_nay_query = TinhThanh.query.filter(TinhThanh.id == tinh_thanh_hien_nay_id).first()

            # add ho khau thuong tru
            if so_nha_thuong_tru is not None and so_nha_thuong_tru != "":
                dia_chi_thuong_tru = so_nha_thuong_tru + ", " + xa_phuong_query.ten + \
                    ", " + quan_huyen_query.ten + ", " + tinh_thanh_query.ten
            else:
                dia_chi_thuong_tru = xa_phuong_query.ten + ", " + quan_huyen_query.ten + ", " + tinh_thanh_query.ten

            quan_ly_nguoi_dung.dia_chi_thuong_tru = dia_chi_thuong_tru

            if request.form.get("mat_khau", False):
                quan_ly_nguoi_dung.tai_khoan.mat_khau = pwd_context.hash(request.form.get("mat_khau"))

             # add cho o hien nay
            if so_nha is not None and so_nha != "":
                dia_chi = so_nha + ", " + xa_phuong_hien_nay_query.ten + ", " + \
                    quan_huyen_hien_nay_query.ten + ", " + tinh_thanh_hien_nay_query.ten
            else:
                dia_chi = xa_phuong_hien_nay_query.ten + ", " + quan_huyen_hien_nay_query.ten + ", " + tinh_thanh_hien_nay_query.ten

            quan_ly_nguoi_dung.dia_chi = dia_chi

            avatar_url = request.files.get("avatar_url")
            if avatar_url is not None:
                try:
                    avatar_url = UploadMinio.upload_duocsi(avatar_url)
                    quan_ly_nguoi_dung.avatar_url = avatar_url
                except:
                    return {"errors": "Tải file thất bại"},  HttpCode.InternalError
        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest

        db.session.commit()
        return {"msg": "Cập nhật thành công", "results": schema.dump(quan_ly_nguoi_dung)}, HttpCode.Created

    @ jwt_required()
    def delete(self, id):
        schema = QuanLyNguoiDungSchema()
        quan_ly_nguoi_dung = User.query.filter(User.id == id).first()
        if quan_ly_nguoi_dung is None:
            return {"errors": "Không có dữ liệu!"},  HttpCode.InternalError
        db.session.delete(quan_ly_nguoi_dung)
        db.session.commit()

        return {"msg": "xóa thành công!"}, HttpCode.OK


class QuanLyNguoiDungUpdateInfo(Resource):
    @jwt_required()
    def put(self, id):
        quan_ly_nguoi_dung: User = User.query.filter(User.id == id).first_or_404()
        if request.json.get("mat_khau", False):
            quan_ly_nguoi_dung.tai_khoan.mat_khau = pwd_context.hash(request.json.get("mat_khau"))
        if request.json.get("chuc_vu", False):
            quan_ly_nguoi_dung.chuc_vu = request.json["chuc_vu"]

        if request.json.get("chuc_vu", None):
            if quan_ly_nguoi_dung.chuc_vu == "0" or quan_ly_nguoi_dung.chuc_vu == "1" or quan_ly_nguoi_dung.chuc_vu == "2" or quan_ly_nguoi_dung.chuc_vu == "3":
                vai_tro = VaiTro.query.filter(VaiTro.ten_en == "lanhdao").first()
            elif quan_ly_nguoi_dung.chuc_vu == "4":
                vai_tro = VaiTro.query.filter(VaiTro.ten_en == "chuyenvien").first()
            elif quan_ly_nguoi_dung.chuc_vu == "5":
                vai_tro = VaiTro.query.filter(VaiTro.ten_en == "chuyenvienhoidong").first()
            elif quan_ly_nguoi_dung.chuc_vu == "6":
                vai_tro = VaiTro.query.filter(VaiTro.ten_en == "vanthu").first()
            else:
                return {
                    "msg": "Chức vụ không phù hợp"
                }, HttpCode.BadRequest
            quan_ly_nguoi_dung.vai_tro_id = vai_tro.id
            db.session.flush()
        if "display_chuc_vu" in request.json and isinstance(request.json["display_chuc_vu"], bool):
            if not request.json["display_chuc_vu"]:
                quan_ly_nguoi_dung.display_chuc_vu = False
            else:
                exist: User = User.query.filter(User.display_chuc_vu == True,
                                                User.chuc_vu == quan_ly_nguoi_dung.chuc_vu).first()
                if exist:
                    return {
                        "msg": f"Cán bộ {exist.ho_ten} đang được hiển thị trong văn bản in với chức vụ này"
                    }, HttpCode.BadRequest
                quan_ly_nguoi_dung.display_chuc_vu = True
        if request.json.get("ho_ten", False):
            ho_ten = request.json["ho_ten"].split(" ")
            quan_ly_nguoi_dung.ho = " ".join(ho_ten[:-1])
            quan_ly_nguoi_dung.ten = ho_ten[-1]

        db.session.commit()
        return {
            "msg": "Cập nhật thành công"
        }, HttpCode.OK


class QuanLyNguoiDungGetList(Resource):
    @ jwt_required()
    def post(self):
        schema = NguoiDungDisplaySchema(many=True)
        query = User.query.filter(User.assigned_role.any(), User.tai_khoan_id != None).filter(User.assigned_role.any(
            and_(not_(VaiTro.ten.like("Dược sĩ")), not_(VaiTro.ten.like("Cơ sở")))))
        data = request.json
        if not data:
            query = query.order_by(User.updated_at.desc())
            return paginate(query, schema), HttpCode.OK

        if data.get("id"):
            id = data["id"]
            query = query.filter(User.id == id)

        if data.get("search_ten", None):
            search_ten = data["search_ten"]
            query = query.filter(User.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
        query = query.order_by(User.ho.asc())
        res = paginate(query, schema)
        if len(res["results"]) < 1:
            return {
                "msg": "Không có tên người dùng!!"
            }, HttpCode.OK

        return res, HttpCode.OK


class QuanLyNguoiDungCreateLanhDao(Resource):
    def post(self):
        data = request.json
        if not data.get("tai_khoan", False):
            return {
                "msg": "Thiếu tài khoản vui lòng nhập lại"
            }, HttpCode.BadRequest
        exist_tai_khoan = TaiKhoan.query.filter(TaiKhoan.tai_khoan.like(data["tai_khoan"])).first()
        if exist_tai_khoan:
            return {
                "msg": "Tên đăng nhập đã tồn tại"
            }, HttpCode.BadRequest

        if not data.get("mat_khau", False):
            return {
                "msg": "Thiếu mật khẩu vui lòng nhập lại"
            }, HttpCode.BadRequest
        created_tai_khoan: TaiKhoan = TaiKhoan(tai_khoan=data["tai_khoan"], mat_khau=data["mat_khau"])
        db.session.add(created_tai_khoan)
        db.session.flush()
        ho_ten = data.get("ho_ten", "").split(" ")

        chuc_vu = data.get("chuc_vu", 0)

        if chuc_vu == "0" or chuc_vu == "1" or chuc_vu == "2" or chuc_vu == "3":
            vai_tro = VaiTro.query.filter(VaiTro.id == "2d2e365c-7f66-4bc3-bd59-8c8ba0ce1100").first()
        elif chuc_vu == "4":
            vai_tro = VaiTro.query.filter(VaiTro.id == "53edce88-7068-4d9c-9c7c-6512f03e47e3").first()
        elif chuc_vu == "5":
            vai_tro = VaiTro.query.filter(VaiTro.id == "da80fc00-ae2f-4bf2-bedf-a5183c8098c3").first()
        elif chuc_vu == "6":
            vai_tro = VaiTro.query.filter(VaiTro.id == "7403d9bf-3a34-494d-93de-f48a7002b06a").first()

        nhan_vien_data = {
            "ho": " ".join(ho_ten[:-1]),
            "ten": ho_ten[-1],
            "chuc_vu": data.get("chuc_vu", 0),
            "tai_khoan_id":  str(created_tai_khoan.id),
        }
        created_nhan_vien: User = QuanLyNguoiDungSchema(
            only=["tai_khoan_id", "ho", "ten", "chuc_vu"]).load(nhan_vien_data)
        created_nhan_vien.assigned_role.append(vai_tro)
        db.session.add(created_nhan_vien)
        db.session.commit()
        return {
            "msg": "Tạo tài khoản thành công"
        }, HttpCode.OK


# class DanhMucChungChiComparision(Resource):
#     def post(self):
#         data = request.json
#         if not data.get("so_giay_phep", None) or None:
#             return {
#                 "msg":"Số giấy phép không tồn tại"
#             }
#         schema = DanhMucChungChiSchema()
#         target_dm_cc = DanhMucChungChi.query.filter(DanhMucChungChi.so_giay_phep == data["so_giay_phep"]).first_or_404()
#         target_dm_cc_json = schema.load(target_dm_cc)
#         diff = []
#         for prop in target_dm_cc_json:
#             if data[prop] == target_dm_cc_json[prop]:
#                 continue
#             diff.append(prop)
#         return {
#             "msg":"Thành công",
#             "results":{
#                 "diff":diff,
#                 "info": target_dm_cc_json
#             }
#         }, HttpCode.OK
