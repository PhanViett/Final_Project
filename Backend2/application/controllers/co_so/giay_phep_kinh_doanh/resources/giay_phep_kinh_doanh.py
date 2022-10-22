from datetime import datetime
import json
from typing import Dict, List
from marshmallow import ValidationError
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from application.extensions import db
from application.models import GiayPhepKinhDoanh, BangCap, CoSoKinhDoanh, DuocSiCoSo, User, ChungChiHanhNghe, LoaiHinhKinhDoanh
from application.models.danhmuc_pham_vi_hoat_dong_kinh_doanh import PhamViHoatDongKinhDoanh
from application.models.danhmuc_van_bang_chuyen_mon import VanBangChuyenMon
from application.models.quan_huyen import QuanHuyen
from application.models.xa_phuong import XaPhuong
from application.schemas.danhmuc_loai_hình_kinh_doanh import LoaiHinhKinhDoanhDisplaySchema
from application.schemas.danhmuc_pham_vi_hoat_dong_kinh_doanh import PhamViHoatDongKinhDoanhDisplaySchema, PhamViHoatDongKinhDoanhParentDisplaySchema
from application.schemas.giay_phep_kinh_doanh import GiayPhepKinhDoanhDisplaySchema, GiayPhepKinhDoanhInfoSchema, GiayPhepKinhDoanhLKDisplaySchema, GiayPhepKinhDoanhSchema
from application.schemas import CoSoKinhDoanhSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
from application.commons.pagination import paginate
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, cast, String, and_


class GiayPhepKinhDoanhPost(Resource):

    @jwt_required()
    def post(self):

        schema = GiayPhepKinhDoanhSchema()

        req = {
            "so_giay_phep": request.json.get("so_giay_phep"),
            "so_giay_phep_before": request.json.get("so_giay_phep_before"),
            "so_giay_phep_after": request.json.get("so_giay_phep_after"),
            "ngay_cap": request.json.get("ngay_cap"),
            "ngay_hieu_luc": request.json.get("ngay_hieu_luc"),
            "ngay_het_han": request.json.get("ngay_het_han"),
            "co_quan_cap": request.json.get("co_quan_cap"),
            "so_giay_gps": request.json.get("so_giay_gps"),
            "thoigian_yeucau_lienket": request.json.get("thoigian_yeucau_lienket"),
            "thoigian_duyet_lienket": request.json.get("thoigian_duyet_lienket"),
            "thoigian_tuchoi_lienket": request.json.get("thoigian_tuchoi_lienket"),
            "lydo_tuchoi_lienket": request.json.get("lydo_tuchoi_lienket"),
            "ma_nguoiduyet": request.json.get("ma_nguoiduyet"),
            "ten_nguoiduyet": request.json.get("ten_nguoiduyet"),
            "tinh_thanh_kinh_doanh_id": request.json.get("tinh_thanh_kinh_doanh_id"),
            "quan_huyen_kinh_doanh_id": request.json.get("quan_huyen_kinh_doanh_id"),
            "xa_phuong_kinh_doanh_id": request.json.get("xa_phuong_kinh_doanh_id"),
            "ghi_chu": request.json.get("ghi_chu"),
            "ghi_chu_loai_hinh_kd": request.json.get("ghi_chu_loai_hinh_kd"),
            "ghi_chu_pham_vi_kd": request.json.get("ghi_chu_pham_vi_kd"),
            "ten_httckd": request.json.get("ten_httckd"),
            "ten_tru_so": request.json.get("ten_tru_so"),
            "dia_chi_tru_so": request.json.get("dia_chi_tru_so"),


        }

        try:
            giay_phep = schema.load(req)
            # giay_phep.nhan_vien_id = current_user.id
            db.session.add(giay_phep)
            db.session.commit()
        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest

        return {"msg": "Tạo giấy phép kinh doanh thành công", "results": schema.dump(giay_phep)}, HttpCode.Created


class GiayPhepKinhDoanhUpdateById(Resource):
    @jwt_required()
    def put(self, id):

        schema = GiayPhepKinhDoanhSchema(partial=True)
        giay_phep = GiayPhepKinhDoanh.query.filter(GiayPhepKinhDoanh.id == id).first()
        if giay_phep is None:
            return {"errors": "No data"},  HttpCode.InternalError

        schema = GiayPhepKinhDoanhSchema()

        req = {
            "so_giay_phep": request.json.get("so_giay_phep"),
            "so_giay_phep_before": request.json.get("so_giay_phep_before"),
            "so_giay_phep_after": request.json.get("so_giay_phep_after"),
            "ngay_cap": request.json.get("ngay_cap"),
            "ngay_hieu_luc": request.json.get("ngay_hieu_luc"),
            "ngay_het_han": request.json.get("ngay_het_han"),
            "co_quan_cap": request.json.get("co_quan_cap"),
            "so_giay_gps": request.json.get("so_giay_gps"),
            "thoigian_yeucau_lienket": request.json.get("thoigian_yeucau_lienket"),
            "thoigian_duyet_lienket": request.json.get("thoigian_duyet_lienket"),
            "thoigian_tuchoi_lienket": request.json.get("thoigian_tuchoi_lienket"),
            "lydo_tuchoi_lienket": request.json.get("lydo_tuchoi_lienket"),
            "ma_nguoiduyet": request.json.get("ma_nguoiduyet"),
            "ten_nguoiduyet": request.json.get("ten_nguoiduyet"),
            "tinh_thanh_kinh_doanh_id": request.json.get("tinh_thanh_kinh_doanh_id"),
            "quan_huyen_kinh_doanh_id": request.json.get("quan_huyen_kinh_doanh_id"),
            "xa_phuong_kinh_doanh_id": request.json.get("xa_phuong_kinh_doanh_id"),
            "ghi_chu": request.json.get("ghi_chu"),
            "ghi_chu_loai_hinh_kd": request.json.get("ghi_chu_loai_hinh_kd"),
            "ghi_chu_pham_vi_kd": request.json.get("ghi_chu_pham_vi_kd"),
            "ten_httckd": request.json.get("ten_httckd"),
            "ten_tru_so": request.json.get("ten_tru_so"),
            "dia_chi_tru_so": request.json.get("dia_chi_tru_so")
        }
        try:
            giay_phep = schema.load(req, instance=giay_phep)
            giay_phep.created_by = current_user.id
        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest
        db.session.commit()
        return {"msg": "Cập nhật thành công", "results": schema.dump(giay_phep)}, HttpCode.OK

    @jwt_required()
    def delete(self, id):
        schema = GiayPhepKinhDoanhSchema()
        giay_phep = GiayPhepKinhDoanh.query.filter(GiayPhepKinhDoanh.id == id).first()
        if giay_phep is None:
            return {"errors": "Không có dữ liệu!"},  HttpCode.InternalError
        db.session.delete(giay_phep)
        db.session.commit()

        return {"msg": "xóa thành công!"}, HttpCode.OK


class GiayPhepkinhDoanhGetList(Resource):
    @jwt_required()
    def post(self):
        schema = GiayPhepKinhDoanhDisplaySchema(many=True)
        query = db.session.query(
            GiayPhepKinhDoanh.id,
            GiayPhepKinhDoanh.co_quan_cap,
            GiayPhepKinhDoanh.so_giay_phep,
            GiayPhepKinhDoanh.ngay_het_han,
            CoSoKinhDoanh.diachi_kinh_doanh,
            CoSoKinhDoanh.so_gcn,
            CoSoKinhDoanh.ten_coso,
            XaPhuong.ten.label("xa_phuong"),
            QuanHuyen.ten.label("quan_huyen"),
            User.ten.label("nguoi_ctncm"))\
            .outerjoin(CoSoKinhDoanh, CoSoKinhDoanh.id == GiayPhepKinhDoanh.co_so_kinh_doanh_id)\
            .outerjoin(DuocSiCoSo, and_(DuocSiCoSo.co_so_kinh_doanh_id == CoSoKinhDoanh.id, DuocSiCoSo.vai_tro == 0))\
            .outerjoin(User, User.id == DuocSiCoSo.duoc_si_id)\
            .outerjoin(XaPhuong, XaPhuong.id == CoSoKinhDoanh.xa_phuong_coso_id)\
            .outerjoin(QuanHuyen, QuanHuyen.id == CoSoKinhDoanh.quan_huyen_coso_id)

        data = request.json
        if data:
            if data.get("search_so_giay_phep"):
                search_so_giay_phep = data["search_so_giay_phep"]
                query = query.filter(GiayPhepKinhDoanh.so_giay_phep.like(f"%{search_so_giay_phep}%"))

            if data.get("search_ten_co_so"):
                search_ten_co_so = data["search_ten_co_so"]
                query = query.filter(CoSoKinhDoanh.ten_coso_khongdau.like(f"%{clean_string(search_ten_co_so)}%"))

            if data.get("search_nctncm"):
                search_nctncm = data["search_nctncm"]
                query = query.filter(User.ten_khong_dau.like(f"%{clean_string(search_nctncm)}%"))

            if data.get("het_han_from"):
                het_han_from = data["het_han_from"]
                query = query.filter(GiayPhepKinhDoanh.ngay_het_han < het_han_from)

            if data.get("het_han_to"):
                het_han_to = data["het_han_to"]
                query = query.filter(GiayPhepKinhDoanh.ngay_het_han < het_han_to)

            if data.get("filter_tinh_trang"):
                filter_tinh_trang = data["filter_tinh_trang"]
                current_time = int(datetime.now().timestamp())
                if filter_tinh_trang:
                    query = query.filter(or_(GiayPhepKinhDoanh.ngay_het_han < current_time,
                                             GiayPhepKinhDoanh.ngay_het_han == None))
                else:
                    query = query.filter(GiayPhepKinhDoanh.ngay_het_han >= current_time)

        res = paginate(query, schema)
        if len(res["results"]) < 1:
            return {
                "msg": "Không giấy phép kinh doanh!"
            }, HttpCode.OK

        target_ids: List[str] = [x["id"] for x in res["results"]]
        lhkd_data = db.session.query(
            cast(GiayPhepKinhDoanh.id, String).label("id"),
            LoaiHinhKinhDoanh.ten
        ).join(GiayPhepKinhDoanh.loai_hinh_kinh_doanh).filter(GiayPhepKinhDoanh.id.in_(target_ids)).all()

        lhkd_res = {}
        for item in lhkd_data:
            data: Dict[str, str] = item._asdict()
            if data["id"] not in lhkd_res:
                lhkd_res[data["id"]] = [data["ten"]]
            else:
                lhkd_res[data["id"]].append(data["ten"])
        for item in res["results"]:
            if lhkd_res.get(item["id"]):
                item["loai_hinh_kinh_doanh"] = lhkd_res[item["id"]]

        return res, HttpCode.OK


class CSKDGetYeuCauLienKet(Resource):
    @ jwt_required()
    def post(self):
        data = request.json
        schema = GiayPhepKinhDoanhLKDisplaySchema(many=True)
        query = db.session.query(
            GiayPhepKinhDoanh.id,
            GiayPhepKinhDoanh.so_giay_phep,
            GiayPhepKinhDoanh.ngay_cap,
            GiayPhepKinhDoanh.ngay_het_han,
            GiayPhepKinhDoanh.thoigian_yeucau_lienket,
            GiayPhepKinhDoanh.trang_thai_ho_so,
            CoSoKinhDoanh.ten_coso,
            CoSoKinhDoanh.diachi_coso
        ).join(CoSoKinhDoanh, GiayPhepKinhDoanh.co_so_kinh_doanh_id == CoSoKinhDoanh.id).filter(CoSoKinhDoanh.taikhoan_id != None)

        if data.get("trang_thai_filter", None) and data["trang_thai_filter"] in ["1", "2", "3"]:
            query = query.filter(GiayPhepKinhDoanh.trang_thai_ho_so == data["trang_thai_filter"])
        else:
            query = query.filter(GiayPhepKinhDoanh.trang_thai_ho_so != '0')
        if data.get("ten_search", None) or None:
            ten_search = data["ten_search"]
            query = query.filter(CoSoKinhDoanh.ten_coso_khongdau.like(
                clean_string(f"%{ten_search}%", clean_white_space=False)))
        if data.get("from_date", None):
            from_date = data.get("from_date")
            query = query.filter(GiayPhepKinhDoanh.thoigian_yeucau_lienket > from_date)
        if data.get("to_date", None):
            to_date = data.get("to_date")
            query = query.filter(GiayPhepKinhDoanh.thoigian_yeucau_lienket < to_date)
        query = query.order_by(GiayPhepKinhDoanh.updated_at.desc())
        return paginate(query, schema), HttpCode.OK


class GPKDGetDisplayInfo(Resource):
    @ jwt_required()
    def get(self):
        if not isinstance(current_user, CoSoKinhDoanh):
            return {
                "msg": "Người dùng không phải là một cơ sở kinh doanh"
            }, HttpCode.BadRequest
        current_co_so: CoSoKinhDoanh = current_user
        current_giay_phep: GiayPhepKinhDoanh = current_co_so.giay_phep_kinh_doanh

        if not current_giay_phep:
            return {
                "msg": "Giấy phép không tồn tại",
            }, HttpCode.NotFound

        res = {
            "msg": "Thành công",
            "results": None
        }

        schema = GiayPhepKinhDoanhInfoSchema()

        res["results"] = schema.dump(current_giay_phep)
        if current_giay_phep.pham_vi_kinh_doanh and len(current_giay_phep.pham_vi_kinh_doanh) > 0:
            pham_vi_kinh_doanh: list[str] = [x.ten for x in current_giay_phep.pham_vi_kinh_doanh]
            pham_vi_kinh_doanh = ", ".join(pham_vi_kinh_doanh)
            res["results"]["pham_vi_kinh_doanh"] = pham_vi_kinh_doanh
        else:
            res["results"]["pham_vi_kinh_doanh"] = None
        if current_giay_phep.loai_hinh_kinh_doanh and len(current_giay_phep.loai_hinh_kinh_doanh) > 0:
            loai_hinh_kinh_doanh: list[str] = [x.ten for x in current_giay_phep.loai_hinh_kinh_doanh]
            loai_hinh_kinh_doanh = ", ".join(loai_hinh_kinh_doanh)
            res["results"]["loai_hinh_kinh_doanh"] = loai_hinh_kinh_doanh
        else:
            res["results"]["loai_hinh_kinh_doanh"] = None

        return res, HttpCode.OK


class GPKDLienKet(Resource):
    @ jwt_required()
    def get(self):
        current_co_so: CoSoKinhDoanh = CoSoKinhDoanh.query\
            .filter_by(id=get_jwt_identity())\
            .options(
                joinedload(CoSoKinhDoanh.giay_phep_kinh_doanh).options(
                    joinedload(GiayPhepKinhDoanh.loai_hinh_kinh_doanh),
                    joinedload(GiayPhepKinhDoanh.pham_vi_kinh_doanh)),
                joinedload(CoSoKinhDoanh.duoc_si_ctncm)
            ).first()
        if not current_co_so:
            return {
                "msg": "Tài khoản phải là cơ sơ kinh doanh"
            }, HttpCode.BadRequest
        res = {
            "thong_tin_co_so": None,
            "thong_tin_nguoi_dung_dau": None,
            "thong_tin_giay_phep": None,
            "nguoi_chiu_trach_nhiem_chuyen_mon": None,
            "pv_hd_kinh_doanh": {
                "danh_sach_pv_hd_kinh_doanh": None,
                "pv_hd_kinh_doanh_checked": None
            }
        }
        res["thong_tin_co_so"] = {
            "ten_co_so": current_co_so.ten_coso,
            "email": current_co_so.email_coso,
            "dia_chi_tru_so_chinh": current_co_so.diachi_coso,
            "dien_thoai": current_co_so.dienthoai_coso,
            "website": current_co_so.website_co_so,
            "ma_so_doanh_nghiep": current_co_so.ma_coso,
            "fax": current_co_so.fax_coso
        }
        res["thong_tin_nguoi_dung_dau"] = {
            "ten_nguoi_lien_he": current_co_so.ten_nguoi_lien_he,
            "chuc_danh": current_co_so.chuc_danh_nguoi_lienhe,
            "dien_thoai": current_co_so.dien_thoai_nguoi_lienhe,
            "email": current_co_so.email_nguoi_lienhe,
            "cmnd": current_co_so.chung_minh_nguoi_lien_he,
            "dia_chi_lien_lac": current_co_so.dia_chi_nguoi_lien_he
        }

        current_duoc_si_ctncm: DuocSiCoSo = current_co_so.duoc_si_ctncm
        if current_duoc_si_ctncm:
            query_sub_data = db.session.query(User.ho_ten, BangCap.ngay_cap,
                                              VanBangChuyenMon.ten, ChungChiHanhNghe.so_giay_phep)\
                .filter(User.id == current_duoc_si_ctncm.duoc_si_id)\
                .outerjoin(BangCap, BangCap.nhan_vien_id == User.id)\
                .outerjoin(ChungChiHanhNghe, ChungChiHanhNghe.nhan_vien_id == User.id)\
                .outerjoin(VanBangChuyenMon, VanBangChuyenMon.id == BangCap.id)\
                .first()
            res["nguoi_chiu_trach_nhiem_chuyen_mon"] = query_sub_data._asdict()

        current_giay_phep: GiayPhepKinhDoanh = current_co_so.giay_phep_kinh_doanh
        if current_giay_phep:
            res["thong_tin_giay_phep"] = {
                "so_giay_phep": current_giay_phep.so_giay_phep,
                "co_quan_cap": current_giay_phep.co_quan_cap,
                "ngay_cap": current_giay_phep.ngay_cap,
                "ngay_hieu_luc": current_giay_phep.ngay_hieu_luc,
                "ngay_het_han": current_giay_phep.ngay_het_han
            }
            res["du_lieu_dinh_kem"] = {
                "dinhkem_chungchi": current_giay_phep.dinh_kem_chung_chi,
                "dinhkem_anh_chandung": current_giay_phep.dinh_kem_anh_chan_dung,
                "dinhkem_vanbang_chuyenmon": current_giay_phep.dinh_kem_van_bang_chuyen_mon,
                "dinhkem_xacnhan_congdan": current_giay_phep.dinh_kem_xac_nhan_cong_dan,
                "dinhkem_files_khac": current_giay_phep.dinh_kem_files_khac
            }

            res["pv_hd_kinh_doanh"]["pv_hd_kinh_doanh_checked"] = [
                x.id for x in current_giay_phep.pham_vi_kinh_doanh] if current_giay_phep.pham_vi_kinh_doanh else []

        danh_sach_pham_vi_kinh_doanh = PhamViHoatDongKinhDoanhParentDisplaySchema(
            many=True).dump(PhamViHoatDongKinhDoanh.query.filter(PhamViHoatDongKinhDoanh.parent_id == None).options(joinedload(PhamViHoatDongKinhDoanh.children)).all())
        res["pv_hd_kinh_doanh"]["danh_sach_pv_hd_kinh_doanh"] = danh_sach_pham_vi_kinh_doanh

        return {
            "msg": "Thành công",
            "results": res
        }, HttpCode.OK


class GPKDLuuThongTin(Resource):
    @ jwt_required()
    def put(self):
        if not request.form.get("so_giay_phep"):
            return {
                "msg": "Thiếu số giấy phép, vui lòng nhập vào"
            }, HttpCode.BadRequest
        data = {
            "so_giay_phep": request.form.get("so_giay_phep"),
            "co_quan_cap": request.form.get("co_quan_cap"),
            "ngay_cap": request.form.get("ngay_cap"),
            "ngay_hieu_luc": request.form.get("ngay_hieu_luc"),
            "ngay_het_han": request.form.get("ngay_het_han")
        }

        # * check if target so_giay_phep exist
        check_existed = GiayPhepKinhDoanh.query.filter(
            GiayPhepKinhDoanh.trang_thai_ho_so == '1',
            GiayPhepKinhDoanh.so_giay_phep.like(data.get("so_giay_phep")),
            GiayPhepKinhDoanh.co_so_kinh_doanh.has(User.tai_khoan_id == None)
        ).first()
        if not check_existed:
            return {
                "msg": "Số giấy phép không tồn tại, vui lòng kiểm tra lại"
            }, HttpCode.BadRequest

        # * get co_so's giay_phep_kinh_doanh
        # * check if it exists
        # * if not, then create new with co_so id
        # * else, then update it
        current_giay_phep: GiayPhepKinhDoanh = GiayPhepKinhDoanh.query.filter(
            GiayPhepKinhDoanh.co_so_kinh_doanh_id == get_jwt_identity()).options(joinedload(GiayPhepKinhDoanh.pham_vi_kinh_doanh)).first()
        if not current_giay_phep:
            current_giay_phep: GiayPhepKinhDoanh = GiayPhepKinhDoanhSchema(only=["so_giay_phep", "co_quan_cap",
                                                                                 "ngay_cap", "ngay_hieu_luc", "ngay_het_han"], exclude=["trang_thai_ho_so", "co_so_kinh_doanh_id"]).load(data)
            current_giay_phep.co_so_kinh_doanh_id = str(get_jwt_identity())
            db.session.add(current_giay_phep)
            db.session.flush()
        else:
            schema = GiayPhepKinhDoanhSchema(only=["so_giay_phep", "co_quan_cap",
                                                   "ngay_cap", "ngay_hieu_luc", "ngay_het_han"], partial=True)
            current_giay_phep = schema.load(instance=current_giay_phep, data=data)
            db.session.flush()

        if request.form.getlist("pham_vi_kinh_doanh_ids[]", None):
            target_pvkd = None
            if len(list(filter(None, request.form.getlist("pham_vi_kinh_doanh_ids[]")))) > 0:
                target_pvkd = PhamViHoatDongKinhDoanh.query.filter(
                    PhamViHoatDongKinhDoanh.id.in_(request.form.getlist("pham_vi_kinh_doanh_ids[]"))).all()
            current_giay_phep.pham_vi_kinh_doanh.clear()
            if target_pvkd:
                current_giay_phep.pham_vi_kinh_doanh = target_pvkd

        upload_errors = []
        # * Upload hinh chup CCHND
        upload_images(images=request.files.getlist("dinh_kem_hinh_chup_cchnd[]"),
                      target_list=current_giay_phep.dinh_kem_chung_chi,
                      error_list=upload_errors)
        remove_images(target_urls=request.form.get("delete_dinh_kem_hinh_chup_cchnd[]"),
                      target_list=current_giay_phep.dinh_kem_chung_chi)

        # * Upload hinh chup chan dung
        upload_images(images=request.files.getlist("dinh_kem_anh_chan_dung[]"),
                      target_list=current_giay_phep.dinh_kem_anh_chan_dung,
                      error_list=upload_errors)
        remove_images(target_urls=request.form.get("delete_dinh_kem_anh_chan_dung[]"),
                      target_list=current_giay_phep.dinh_kem_anh_chan_dung)

        # * Upload hinh chup cmnd
        upload_images(images=request.files.getlist("dinh_kem_cmnd[]"),
                      target_list=current_giay_phep.dinh_kem_xac_nhan_cong_dan,
                      error_list=upload_errors)
        remove_images(target_urls=request.form.get("delete_dinh_kem_cmnd[]"),
                      target_list=current_giay_phep.dinh_kem_xac_nhan_cong_dan)

        # * Upload hinh chup khac
        upload_images(images=request.files.getlist("dinh_kem_khac[]"),
                      target_list=current_giay_phep.dinh_kem_xac_nhan_khac,
                      error_list=upload_errors)
        remove_images(target_urls=request.form.get("delete_dinh_kem_khac[]"),
                      target_list=current_giay_phep.dinh_kem_xac_nhan_khac)
        db.session.commit()
        return {
            "msg": "Lưu thông tin thành công",
            "upload_errors": upload_errors
        }, HttpCode.OK


class GPKDGuiDeNghiLienKet(Resource):
    @ jwt_required()
    def put(self):
        if not request.form.get("so_giay_phep"):
            return {
                "msg": "Thiếu số giấy phép, vui lòng nhập vào"
            }, HttpCode.BadRequest
        data = {
            "so_giay_phep": request.form.get("so_giay_phep"),
            "co_quan_cap": request.form.get("co_quan_cap"),
            "ngay_cap": request.form.get("ngay_cap"),
            "ngay_hieu_luc": request.form.get("ngay_hieu_luc"),
            "ngay_het_han": request.form.get("ngay_het_han")
        }

        # * check if target so_giay_phep exist
        check_existed = GiayPhepKinhDoanh.query.filter(
            GiayPhepKinhDoanh.trang_thai_ho_so == '1',
            GiayPhepKinhDoanh.so_giay_phep.like(data.get("so_giay_phep")),
            GiayPhepKinhDoanh.co_so_kinh_doanh.has(User.tai_khoan_id == None)
        ).first()
        if not check_existed:
            return {
                "msg": "Số giấy phép không tồn tại, vui lòng kiểm tra lại"
            }, HttpCode.BadRequest

        # * get co_so's giay_phep_kinh_doanh
        # * check if it exists
        # * if not, then create new with co_so id
        # * else, then update it
        current_giay_phep: GiayPhepKinhDoanh = GiayPhepKinhDoanh.query.filter(
            GiayPhepKinhDoanh.co_so_kinh_doanh_id == get_jwt_identity()).options(joinedload(GiayPhepKinhDoanh.pham_vi_kinh_doanh)).first()
        if not current_giay_phep:
            current_giay_phep: GiayPhepKinhDoanh = GiayPhepKinhDoanhSchema(only=["so_giay_phep", "co_quan_cap",
                                                                                 "ngay_cap", "ngay_hieu_luc", "ngay_het_han"], exclude=["trang_thai_ho_so", "co_so_kinh_doanh_id"]).load(data)
            current_giay_phep.co_so_kinh_doanh_id = str(get_jwt_identity())
            current_giay_phep.trang_thai_ho_so = 1
            db.session.add(current_giay_phep)
            db.session.flush()
        else:
            schema = GiayPhepKinhDoanhSchema(only=["so_giay_phep", "co_quan_cap",
                                                   "ngay_cap", "ngay_hieu_luc", "ngay_het_han"], partial=True)
            current_giay_phep = schema.load(instance=current_giay_phep, data=data)
            current_giay_phep.trang_thai_ho_so = 1
            db.session.flush()

        if request.form.getlist("pham_vi_kinh_doanh_ids[]", None):
            target_pvkd = None
            if len(list(filter(None, request.form.getlist("pham_vi_kinh_doanh_ids[]")))) > 0:
                target_pvkd = PhamViHoatDongKinhDoanh.query.filter(
                    PhamViHoatDongKinhDoanh.id.in_(request.form.getlist("pham_vi_kinh_doanh_ids[]"))).all()
            current_giay_phep.pham_vi_kinh_doanh.clear()
            if target_pvkd:
                current_giay_phep.pham_vi_kinh_doanh = target_pvkd

        upload_errors = []
        # * Upload hinh chup CCHND
        danh_sach_hinh_chup_cchnd = request.files.getlist("dinh_kem_hinh_chup_cchnd[]")
        if danh_sach_hinh_chup_cchnd and len(danh_sach_hinh_chup_cchnd) > 0:
            danh_sach_link_cchnd, errors = UploadMinio.upload_duocsi(danh_sach_hinh_chup_cchnd, many=True)
            if current_giay_phep.dinh_kem_chung_chi:
                current_giay_phep.dinh_kem_chung_chi.extend(danh_sach_link_cchnd)
            else:
                current_giay_phep.dinh_kem_chung_chi = danh_sach_link_cchnd
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_hinh_chup_cchnd[]") and current_giay_phep.dinh_kem_chung_chi:
            current_giay_phep.dinh_kem_chung_chi = [
                x for x in current_giay_phep.dinh_kem_chung_chi if x["url"] not in request.form.getlist("delete_dinh_kem_hinh_chup_cchnd[]")]

        # * Upload hinh chup chan dung
        danh_sach_anh_chan_dung = request.files.getlist("dinh_kem_anh_chan_dung[]")
        if danh_sach_anh_chan_dung and len(danh_sach_anh_chan_dung) > 0:
            danh_sach_link_chan_dung, errors = UploadMinio.upload_duocsi(danh_sach_anh_chan_dung, many=True)
            if current_giay_phep.dinh_kem_anh_chan_dung:
                current_giay_phep.dinh_kem_anh_chan_dung.extend(danh_sach_link_chan_dung)
            else:
                current_giay_phep.dinh_kem_anh_chan_dung = danh_sach_link_chan_dung
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_anh_chan_dung[]") and current_giay_phep.dinh_kem_anh_chan_dung:
            current_giay_phep.dinh_kem_anh_chan_dung = [
                x for x in current_giay_phep.dinh_kem_anh_chan_dung if x["url"] not in request.form.getlist("delete_dinh_kem_anh_chan_dung[]")]

        # * Upload hinh chup cmnd
        danh_sach_cmnd = request.files.getlist("dinh_kem_cmnd[]")
        if danh_sach_cmnd and len(danh_sach_cmnd) > 0:
            danh_sach_link_cmnd, errors = UploadMinio.upload_duocsi(danh_sach_cmnd, many=True)
            if current_giay_phep.dinh_kem_xac_nhan_cong_dan:
                current_giay_phep.dinh_kem_xac_nhan_cong_dan.extend(danh_sach_link_cmnd)
            else:
                current_giay_phep.dinh_kem_xac_nhan_cong_dan = danh_sach_link_cmnd
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_cmnd[]") and current_giay_phep.dinh_kem_xac_nhan_cong_dan:
            current_giay_phep.dinh_kem_xac_nhan_cong_dan = [
                x for x in current_giay_phep.dinh_kem_xac_nhan_cong_dan if x["url"] not in request.form.getlist("delete_dinh_kem_cmnd[]")]

        # * Upload hinh chup khac
        danh_sach_khac = request.files.getlist("dinh_kem_khac[]")
        if danh_sach_khac and len(danh_sach_khac) > 0:
            danh_sach_link_khac, errors = UploadMinio.upload_duocsi(danh_sach_khac, many=True)
            if current_giay_phep.dinh_kem_xac_nhan_khac:
                current_giay_phep.dinh_kem_xac_nhan_khac.extend(danh_sach_link_khac)
            else:
                current_giay_phep.dinh_kem_xac_nhan_khac = danh_sach_link_khac
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_khac[]") and current_giay_phep.dinh_kem_xac_nhan_khac:
            current_giay_phep.dinh_kem_xac_nhan_khac = [
                x for x in current_giay_phep.dinh_kem_xac_nhan_khac if x["url"] not in request.form.getlist("delete_dinh_kem_khac[]")]

        db.session.commit()
        return {
            "msg": "Lưu thông tin thành công",
            "upload_errors": upload_errors
        }, HttpCode.OK


class GPKDCompare(Resource):
    @ jwt_required()
    def get(self, id):
        schema_giay_phep_cung_cap = GiayPhepKinhDoanhSchema(
            only=["id", "so_giay_phep", "co_quan_cap", "ngay_hieu_luc", "ngay_het_han", "trang_thai_ho_so",
                  "dinh_kem_chung_chi", "dinh_kem_anh_chan_dung", "dinh_kem_xac_nhan_cong_dan", "dinh_kem_files_khac"])
        schema_giay_phep_thong_tin = GiayPhepKinhDoanhSchema(
            only=["so_giay_phep", "co_quan_cap", "ngay_hieu_luc", "ngay_het_han", "trang_thai_ho_so"])
        schema_co_so = CoSoKinhDoanhSchema(only=["ten_coso", "diachi_kinh_doanh"])

        diff_list = []
        res = {"thong_tin_cung_cap": {
            "id": None,
            "ten_coso": None,
            "diachi_kinh_doanh": None,
            "so_giay_phep": None,
            "co_quan_cap": None,
            "ngay_hieu_luc": None,
            "ngay_het_han": None,
            "trang_thai_ho_so": None,
            "duoc_si_ctncm": None,
            "dinh_kem_anh_xac_nhan_cong_dan": [],
            "dinh_kem_files_khac": [],
            "dinh_kem_anh_chan_dung": [],
            "dinh_kem_chung_chi": []
        },
            "thong_tin_giay_phep": {
            "ten_coso": None,
            "diachi_kinh_doanh": None,
            "so_giay_phep": None,
            "co_quan_cap": None,
            "ngay_hieu_luc": None,
            "ngay_het_han": None,
            "trang_thai_ho_so": None,
            "duoc_si_ctncm": None,
            "pham_vi_kinh_doanh": None,
            "loai_hinh_kinh_doanh": None
        },
            "diff": []}

        giay_phep_moi: GiayPhepKinhDoanh = GiayPhepKinhDoanh.query.filter(
            GiayPhepKinhDoanh.id == id, GiayPhepKinhDoanh.co_so_kinh_doanh.has(CoSoKinhDoanh.taikhoan_id != None))\
            .options(joinedload(GiayPhepKinhDoanh.co_so_kinh_doanh)
                     .options(joinedload(CoSoKinhDoanh.duoc_si_ctncm))).first_or_404()

        giay_phep_cu: GiayPhepKinhDoanh = GiayPhepKinhDoanh.query.filter(
            GiayPhepKinhDoanh.so_giay_phep.like(giay_phep_moi.so_giay_phep), GiayPhepKinhDoanh.co_so_kinh_doanh.has(CoSoKinhDoanh.taikhoan_id == None))\
            .options(joinedload(GiayPhepKinhDoanh.co_so_kinh_doanh)
                     .options(joinedload(CoSoKinhDoanh.duoc_si_ctncm)),
                     joinedload(GiayPhepKinhDoanh.loai_hinh_kinh_doanh),
                     joinedload(GiayPhepKinhDoanh.pham_vi_kinh_doanh)).first_or_404()

        res["thong_tin_cung_cap"].update(schema_giay_phep_cung_cap.dump(giay_phep_moi)) if giay_phep_moi else None
        res["thong_tin_giay_phep"].update(schema_giay_phep_thong_tin.dump(giay_phep_cu)) if giay_phep_cu else None

        res["thong_tin_cung_cap"].update(schema_co_so.dump(giay_phep_moi.co_so_kinh_doanh))
        res["thong_tin_giay_phep"].update(schema_co_so.dump(giay_phep_cu.co_so_kinh_doanh))
        res["thong_tin_giay_phep"]["loai_hinh_kinh_doanh"] = ", ".join(
            [x.ten for x in giay_phep_cu.loai_hinh_kinh_doanh]) if len(giay_phep_cu.loai_hinh_kinh_doanh) > 0 else None
        res["thong_tin_giay_phep"]["pham_vi_kinh_doanh"] = ", ".join(
            [x.ten for x in giay_phep_cu.pham_vi_kinh_doanh]) if len(giay_phep_cu.pham_vi_kinh_doanh) > 0 else None

        if giay_phep_moi and giay_phep_moi.co_so_kinh_doanh.duoc_si_ctncm:
            duoc_si_ctncm_data_moi = db.session.query(User.ho_ten, BangCap.ngay_cap, VanBangChuyenMon.ten, ChungChiHanhNghe.so_giay_phep)\
                .filter(User.id == giay_phep_moi.co_so_kinh_doanh.duoc_si_ctncm.id)\
                .outerjoin(BangCap, BangCap.nhan_vien_id == User.id)\
                .outerjoin(ChungChiHanhNghe, ChungChiHanhNghe.nhan_vien_id == User.id)\
                .outerjoin(VanBangChuyenMon, VanBangChuyenMon.id == BangCap.id)\
                .first()
            if duoc_si_ctncm_data_moi:
                res["thong_tin_cung_cap"]["duoc_si_ctncm"].update(duoc_si_ctncm_data_moi._asdict)

        if giay_phep_cu and giay_phep_cu.co_so_kinh_doanh.duoc_si_ctncm:
            duoc_si_ctncm_data_cu = db.session.query(User.ho_ten, BangCap.ngay_cap, VanBangChuyenMon.ten, ChungChiHanhNghe.so_giay_phep)\
                .filter(User.id == giay_phep_moi.trac)\
                .outerjoin(BangCap, BangCap.nhan_vien_id == User.id)\
                .outerjoin(ChungChiHanhNghe, ChungChiHanhNghe.nhan_vien_id == User.id)\
                .outerjoin(VanBangChuyenMon, VanBangChuyenMon.id == BangCap.id)\
                .first()
            if duoc_si_ctncm_data_cu:
                res["thong_tin_cung_cap"]["duoc_si_ctncm"].update(duoc_si_ctncm_data_cu._asdict)

        for key, value in res["thong_tin_cung_cap"].items():
            # * if key doesn't exist, skip
            if key not in res["thong_tin_giay_phep"]:
                continue
            if res["thong_tin_giay_phep"][key] == value:
                continue
            res["diff"].append(key)

        return {
            "msg": "Thành công",
            "results": res
        }


class GPKDDuyetLienKet(Resource):
    @ jwt_required()
    def put(self, id):
        try:
            current_giay_phep: GiayPhepKinhDoanh = GiayPhepKinhDoanh.query.filter(
                GiayPhepKinhDoanh.id == id).first_or_404()
            previous_giay_phep: GiayPhepKinhDoanh = GiayPhepKinhDoanh.query.filter(
                GiayPhepKinhDoanh.trang_thai_ho_so == '1', GiayPhepKinhDoanh.so_giay_phep.like(current_giay_phep.so_giay_phep), GiayPhepKinhDoanh.co_so_kinh_doanh.has(User.tai_khoan_id == None)).first()

            current_giay_phep.trang_thai_ho_so = 2
            previous_giay_phep.trang_thai_ho_so = '2'
            db.session.commit()
            return {
                "msg": "Liên kết thành công"
            }
        except Exception as e:
            return {
                "msg": "Đã xảy ra lỗi khi liên kết chứng chỉ, vui lòng thử lại sau",
                "error": e.args[0]
            }, HttpCode.BadRequest


class GPKDTuChoiLienKet(Resource):
    @ jwt_required()
    def put(self, id):
        try:
            current_giay_phep: GiayPhepKinhDoanh = GiayPhepKinhDoanh.query.filter(
                GiayPhepKinhDoanh.id == id).first_or_404()
            current_giay_phep.trang_thai_ho_so = '3'
            previous_giay_phep: GiayPhepKinhDoanh = GiayPhepKinhDoanh.query.filter(
                GiayPhepKinhDoanh.so_giay_phep.like(current_giay_phep.so_giay_phep), GiayPhepKinhDoanh.co_so_kinh_doanh.has(User.tai_khoan_id == None)).first()
            previous_giay_phep.trang_thai_ho_so = '1'

            db.session.commit()
            return {
                "msg": "Từ chối liên kết thành công"
            }
        except Exception as e:
            return {
                "msg": "Đã xảy ra lỗi khi thực hiện lệnh, vui lòng thử lại sau",
                "error": e.args[0]
            }, HttpCode.BadRequest


def upload_images(images, target_list, error_list=[]):
    if images and len(images) > 0:
        links, errors = UploadMinio.upload_duocsi(images, many=True)
        if target_list:
            target_list.extend(links)
        else:
            target_list[:] = links
        if errors:
            error_list.extend(errors)


def remove_images(target_urls, target_list):
    if target_urls and len(target_urls) > 0 and target_list:
        target_list[:] = [image for image in target_list if image["url"]
                          not in target_urls]
