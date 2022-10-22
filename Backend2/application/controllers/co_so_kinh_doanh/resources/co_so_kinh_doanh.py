
from re import L
from flask import request
from flask_restful import Resource
from flask_jwt_extended import current_user, jwt_required
from application.models.co_so_kinh_doanh import CoSoKinhDoanh
from application.models.danhmuc_loai_hinh_kinh_doanh import LoaiHinhKinhDoanh
from application.models.danhmuc_pham_vi_hoat_dong_kinh_doanh import PhamViHoatDongKinhDoanh
from application.models.tinh_thanh import TinhThanh
from application.models.quan_huyen import QuanHuyen
from application.models.xa_phuong import XaPhuong
from application.schemas.co_so_kinh_doanh import CoSoKinhDoanhSchema
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
from application.extensions import db
from application.utils.helper.string_processing_helper import clean_string
from application.commons.pagination import paginate
from application.utils.validate.uuid_validator import is_valid_uuid


class CoSoKinhDoanhResource(Resource):
    # add oke
    @jwt_required()
    def post(self):
        schema = CoSoKinhDoanhSchema()
        req = {
            "nguoi_tncm_id": request.form.get("nguoi_tncm_id"),
            "taikhoan_id": request.form.get("taikhoan_id"),
            "ma_coso": request.form.get("ma_coso"),
            "ten_coso": request.form.get("ten_coso"),
            "email_coso": request.form.get("email_coso"),
            "dienthoai_coso": request.form.get("dienthoai_coso"),
            "fax_coso": request.form.get("fax_coso"),
            "avatar_url": request.form.get("avatar_url"),
            "so_giay_phep_before": request.form.get("so_giay_phep_before"),
            "so_giay_phep_after": request.form.get("so_giay_phep_after"),
            "ngay_cap": request.form.get("ngay_cap"),
            "ngay_hieu_luc": request.form.get("ngay_hieu_luc"),
            "ngay_het_han": request.form.get("ngay_het_han"),
            "co_quan_cap": request.form.get("co_quan_cap"),
            "thoigian_yeucau_lienket": request.form.get("thoigian_yeucau_lienket"),
            "thoigian_duyet_lienket": request.form.get("thoigian_duyet_lienket"),
            "ma_nguoiduyet": request.form.get("ma_nguoiduyet"),
            "ten_nguoiduyet": request.form.get("ten_nguoiduyet"),
            "thoigian_tuchoi_lienket": request.form.get("thoigian_tuchoi_lienket"),
            "lydo_tuchoi_lienket": request.form.get("lydo_tuchoi_lienket"),
            "trang_thai": request.form.get("trang_thai"),
            "diachi_coso": request.form.get("diachi_coso"),
            "diachi_kho": request.form.get("diachi_kho"),
            "ten_kinhdoanh": request.form.get("ten_kinhdoanh"),
            "diachi_kinh_doanh": request.form.get("diachi_kinh_doanh"),
            "ten_nguoi_lien_he": request.form.get("ten_nguoi_lien_he"),
            "chuc_danh_nguoi_lienhe": request.form.get("chuc_danh_nguoi_lienhe"),
            "email_nguoi_lienhe": request.form.get("email_nguoi_lienhe"),
            "dien_thoai_nguoi_lienhe": request.form.get("dien_thoai_nguoi_lienhe"),
            "fax_nguoi_lienhe": request.form.get("fax_nguoi_lienhe"),
            "truc_thuoc": request.form.get("truc_thuoc"),
            "ten_truc_thuoc": request.form.get("ten_truc_thuoc"),
            "diachi_tructhuoc": request.form.get("diachi_tructhuoc"),
            "website_co_so": request.form.get('website_co_so'),
            "chung_minh_nguoi_lien_he": request.form.get('chung_minh_nguoi_lien_he'),
            "maso_doanh_nghiep_kinh_doanh": request.form.get('maso_doanh_nghiep_kinh_doanh'),
            "ma_so_doanh_nghiep_chi_nhanh": request.form.get('ma_so_doanh_nghiep_chi_nhanh'),
            "dia_chi_nguoi_lien_he": request.form.get('dia_chi_nguoi_lien_he')
        }
        
        so_giay_phep = request.form.get("so_giay_phep")
        chung_nhan_exist = CoSoKinhDoanh.query.filter(CoSoKinhDoanh.so_giay_phep == so_giay_phep).first()
        if chung_nhan_exist is not None:
            return {"msg": "Số giấy phép đã tồn tại"},  HttpCode.BadRequest
        co_so_kinh_doanh: CoSoKinhDoanh = schema.load(req)
        co_so_kinh_doanh.taikhoan_id = current_user.id

        if 'dinhkem_chungchi' in request.files:
            try:
                dinhkem_chungchi = request.files['dinhkem_chungchi']
                chung_chi = UploadMinio.upload_duocsi(dinhkem_chungchi)
                co_so_kinh_doanh.dinhkem_chungchi = chung_chi
            except:
                return {"msg": "Tải Đính Kèm Thất Bại"},  HttpCode.InternalError

        if 'dinhkem_anh_chandung' in request.files:
            try:
                dinhkem_anh_chandung = request.files['dinhkem_anh_chandung']
                chan_dung = UploadMinio.upload_duocsi(dinhkem_anh_chandung)
                co_so_kinh_doanh.dinhkem_anh_chandung = chan_dung
            except:
                return {"msg": "Tải Đính Kèm Thất Bại"},  HttpCode.InternalError

        if 'dinhkem_vanbang_chuyenmon' in request.files:
            try:
                dinhkem_vanbang_chuyenmon = request.files['dinhkem_vanbang_chuyenmon']
                vang_bang = UploadMinio.upload_duocsi(dinhkem_vanbang_chuyenmon)
                co_so_kinh_doanh.dinhkem_vanbang_chuyenmon = vang_bang
            except:
                return {"msg": "Tải Đính Kèm Thất Bại"},  HttpCode.InternalError
        if 'dinhkem_xacnhan_congdan' in request.files:
            try:
                dinhkem_xacnhan_congdan = request.files['dinhkem_xacnhan_congdan']
                cong_dan = UploadMinio.upload_duocsi(dinhkem_xacnhan_congdan)
                co_so_kinh_doanh.dinhkem_xacnhan_congdan = cong_dan
            except:
                return {"msg": "Tải Đính Kèm Thất Bại"},  HttpCode.InternalError
        if 'dinhkem_files_khac' in request.files:
            try:
                dinhkem_files_khac = request.files['dinhkem_files_khac']
                file_khac = UploadMinio.upload_duocsi(dinhkem_files_khac)
                co_so_kinh_doanh.dinhkem_files_khac = file_khac
            except:
                return {"msg": "Tải Đính Kèm Thất Bại"},  HttpCode.InternalError
         # ! relationship

        pham_vi_kinh_doanh_ids = request.form.getlist("pham_vi_kinh_doanh_ids")

        pham_vi_kinh_doanhs = PhamViHoatDongKinhDoanh.query.filter(
            PhamViHoatDongKinhDoanh.id.in_(pham_vi_kinh_doanh_ids)).all()
        for pham_vi_kinh_doanh in pham_vi_kinh_doanhs:
            co_so_kinh_doanh.pham_vi_kinh_doanh.append(pham_vi_kinh_doanh)

        loai_hinh_kinh_doanh_id = request.form.getlist("loai_hinh_kinh_doanh_id")
        loai_hinh_kinh_doanhs = LoaiHinhKinhDoanh.query.filter(LoaiHinhKinhDoanh.id.in_(loai_hinh_kinh_doanh_id)).all()
        for loai_hinh_kinh_doanh in loai_hinh_kinh_doanhs:
            co_so_kinh_doanh.loai_hinh_kinh_doanh.append(loai_hinh_kinh_doanh)

        db.session.add(co_so_kinh_doanh)
        db.session.commit()

        return schema.dump(co_so_kinh_doanh), HttpCode.OK


class CoSoKinhDoanhById(Resource):
    @jwt_required()
    def put(self, id):
        # data = request.json

        data = {
                "ten_coso": request.form.get("ten_coso"),
                "ma_coso": request.form.get("ma_coso"),
                "website_co_so": request.form.get('website_co_so'),
                "ngay_cap": request.form.get("ngay_cap"),
                "email_coso": request.form.get("email_coso"),
                "dienthoai_coso": request.form.get("dienthoai_coso"),
                "fax_coso": request.form.get("fax_coso"),
                "tinh_thanh_coso_id": request.form.get("tinh_thanh_coso_id"),  
                "quan_huyen_coso_id": request.form.get("quan_huyen_coso_id"),  
                "xa_phuong_coso_id": request.form.get("xa_phuong_coso_id"),  
                "tinh_thanh_tructhuoc_id": request.form.get("tinh_thanh_tructhuoc_id"),  
                "quan_huyen_tructhuoc_id": request.form.get("quan_huyen_tructhuoc_id"),  
                "xa_phuong_tructhuoc_id": request.form.get("xa_phuong_tructhuoc_id"),  
                "diachi_coso": request.form.get("diachi_coso"),
                "diachi_tructhuoc": request.form.get("diachi_tructhuoc"),
                "ten_nguoi_lien_he": request.form.get("ten_nguoi_lien_he"),
                "chuc_danh_nguoi_lienhe": request.form.get("chuc_danh_nguoi_lienhe"),
                "email_nguoi_lienhe": request.form.get("email_nguoi_lienhe"),
                "dien_thoai_nguoi_lienhe": request.form.get("dien_thoai_nguoi_lienhe"),
                "dia_chi_nguoi_lien_he": request.form.get('dia_chi_nguoi_lien_he'),
                "ten_truc_thuoc": request.form.get("ten_truc_thuoc"),
                "ma_tructhuoc": request.form.get("ma_tructhuoc"),
            }

        schema = CoSoKinhDoanhSchema(exclude=["id_mapping", "taikhoan_id"], partial=True)
        co_so_kinh_doanh = CoSoKinhDoanh.query.filter(CoSoKinhDoanh.id == id).first()
        if co_so_kinh_doanh is None:
            return {"errors": "No data"},  HttpCode.InternalError
        if not is_valid_uuid(id):
            return {
                "errorCode":"EC05",
                "msg":"ID sai định dạng (không phải UUID)"
            }
        quan_ly_to_chuc:CoSoKinhDoanh = schema.load(data)

        if data["tinh_thanh_coso_id"] is not None:
            quan_ly_to_chuc.tinh_thanh_coso_id = data["tinh_thanh_coso_id"]
        if data["quan_huyen_coso_id"] is not None:
            quan_ly_to_chuc.quan_huyen_coso_id = data["quan_huyen_coso_id"]
        if data["xa_phuong_coso_id"] is not None:
            quan_ly_to_chuc.xa_phuong_coso_id = data["xa_phuong_coso_id"]
        
        if data["tinh_thanh_tructhuoc_id"] is not None:
            quan_ly_to_chuc.tinh_thanh_tructhuoc_id = data["tinh_thanh_tructhuoc_id"]
        if data["quan_huyen_tructhuoc_id"] is not None:
            quan_ly_to_chuc.quan_huyen_tructhuoc_id = data["quan_huyen_tructhuoc_id"]
        if data["xa_phuong_tructhuoc_id"] is not None:
            quan_ly_to_chuc.xa_phuong_tructhuoc_id = data["xa_phuong_tructhuoc_id"]


        avatar_url = request.files.get("avatar_url")
        if avatar_url is not None:
            try:
                avatar_url = UploadMinio.upload_duocsi(avatar_url)
                quan_ly_to_chuc.avatar_url = avatar_url
            except:
                return {"errors": "Tải file thất bại"},  HttpCode.InternalError


        co_so_kinh_doanh = schema.load(instance=co_so_kinh_doanh, data=data)
        db.session.commit()

        return {"msg": "Cập nhật thành công", "results": schema.dump(co_so_kinh_doanh)}, HttpCode.OK

    @jwt_required()
    def get(self, id):
        schema = CoSoKinhDoanhSchema()
        co_so = CoSoKinhDoanh.query.filter(CoSoKinhDoanh.id == id).first()
        if co_so is None:
            return {"errors": "No data"},  HttpCode.InternalError
        return {
            "result": { schema.dump(co_so) }
        }, HttpCode.OK

class CoSoKinhDoanhGetList(Resource):
    def get(self):
        schema = CoSoKinhDoanhSchema()
        query = CoSoKinhDoanh.query
        ten_coso = request.args.get("ten_coso")
        if ten_coso is None:
            list = query
        else:
            list = query.filter(CoSoKinhDoanh.ten_coso_khongdau.like(f"%{clean_string(ten_coso)}%"))
        
        return paginate(list, schema), HttpCode.OK