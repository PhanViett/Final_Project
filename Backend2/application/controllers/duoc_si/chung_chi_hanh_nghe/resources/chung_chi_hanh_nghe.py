from datetime import datetime
import json
from flask_restful import Resource
from application.models.bang_cap import BangCap
from application.models.bang_thong_bao import ThongBao
from application.models.chung_chi_hanh_nghe import ChungChiHanhNghe
from application.models.danhmuc_pham_vi_hoat_dong_chuyen_mon import PhamViHoatDongChuyenMon
from application.models.danhmuc_van_bang_chuyen_mon import VanBangChuyenMon
from application.models.danhmuc_vi_tri_hanh_nghe import ViTriHanhNghe
from application.models.user import User
from application.schemas.bang_cap import BangCapNguoiHanhNgheSchema, BangCapSchema
from application.schemas.chung_chi_hanh_nghe import CCHNDaCapDisplay, CCHNInfoSchema, ChungChiHanhNgheSchema, ChungChiHanhNgheDisplaySchema
from flask_jwt_extended import jwt_required, current_user
from flask import request
from application.schemas.danhmuc_van_bang_chuyen_mon import VanBangChuyenMonDisplaySchema, VanBangChuyenMonSchema
from application.schemas.nhan_vien import NguoiDungDisplaySchema, NhanVienHanhNgheSchema, NhanVienSchema, ThongTinHanhChinhSchema
from application.schemas.danhmuc_pham_vi_hoat_dong_chuyen_mon import PhamViHoatDongChuyenMonDisplaySchema, PhamViHoatDongChuyenMonSchema
from application.schemas.danhmuc_vi_tri_hanh_nghe import ViTriHanhNgheDisplaySchema, ViTriHanhNgheParentDisplaySchema, ViTriHanhNgheSchema
from application.schemas.nhan_vien import NhanVienSchema
from application.utils.helper.push_notification_helper import send_push_notification
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from application.utils.helper.upload_minio import UploadMinio
from application.extensions import db, redisdb
from application.commons.pagination import paginate
from sqlalchemy import and_, extract
from sqlalchemy.orm import joinedload, subqueryload, noload
import time


class ChungChiHanhNgheGetList(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        schema = ChungChiHanhNgheDisplaySchema(many=True)
        query = db.session.query(ChungChiHanhNghe.id.label("id"),
                                 ChungChiHanhNghe.trang_thai_ho_so.label("trang_thai"),
                                 ChungChiHanhNghe.thoi_gian_yeu_cau_lien_ket.label("thoi_gian_lien_ket"),
                                 User.ho_ten.label("ho_ten"),
                                 User.ngay_sinh.label("ngay_sinh"),
                                 User.gioi_tinh.label("gioi_tinh"),
                                 ).join(User, User.id == ChungChiHanhNghe.nhan_vien_id).filter(User.tai_khoan_id != None)
        if data.get("trang_thai_filter", None) and data["trang_thai_filter"] in ["1", "2", "3"]:
            query = query.filter(ChungChiHanhNghe.trang_thai_ho_so == data["trang_thai_filter"])
        else:
            query = query.filter(ChungChiHanhNghe.trang_thai_ho_so != '0')
        if data.get("ten_search", None) or None:
            ten_search = data["ten_search"]
            query = query.filter(User.ten_khong_dau.like(clean_string(f"%{ten_search}%", clean_white_space=False)))
        if data.get("from_date", None):
            from_date = data.get("from_date")
            query = query.filter(ChungChiHanhNghe.thoi_gian_yeu_cau_lien_ket > from_date)
        if data.get("to_date", None):
            to_date = data.get("to_date")
            query = query.filter(ChungChiHanhNghe.thoi_gian_yeu_cau_lien_ket < to_date)
        query = query.order_by(ChungChiHanhNghe.updated_at.desc())
        return paginate(query, schema), HttpCode.OK


class CCHNDaCapGetList(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        schema = CCHNDaCapDisplay(many=True)
        query = ChungChiHanhNghe.query.join(
            User, and_(User.id == ChungChiHanhNghe.nhan_vien_id, User.da_cap_chung_chi == True)).filter(User.tai_khoan_id != None)\
            .options(noload(ChungChiHanhNghe.pham_vi_chuyen_mon),
                     noload(ChungChiHanhNghe.vi_tri_hanh_nghe),
                     noload(ChungChiHanhNghe.van_bang_chuyen_mon))

        if data.get("ten_search", None) or None:
            ten_search = data["ten_search"]
            query = query.filter(User.ten_khong_dau.like(clean_string(f"%{ten_search}%", clean_white_space=False)))

        return paginate(query, schema), HttpCode.OK


class ChungChiHanhNgheCreate(Resource):

    @ jwt_required()
    def post(self):

        schema = ChungChiHanhNgheSchema()

        req = {
            "van_bang_chuyen_mon_id": request.form.get("van_bang_chuyen_mon_id"),
            "so_giay_phep": request.form.get("so_giay_phep"),
            "co_quan_cap": request.form.get("co_quan_cap"),
            "ngay_hieu_luc": request.form.get("ngay_hieu_luc"),
            "nam_cap": request.form.get("nam_cap"),
            "noi_cong_tac": request.form.get("noi_cong_tac"),
            "dia_chi_cong_tac": request.form.get("dia_chi_cong_tac"),
            "hinh_thuc": request.form.get("hinh_thuc"),

            # "yeu_cau_phien_dich": request.form.get("yeu_cau_phien_dich"),
            # "so_quyet_dinh": request.form.get("so_quyet_dinh"),
            # "ngay_quyet_dinh": request.form.get("ngay_quyet_dinh"),

            #  ! upload files
            # "dinh_kem_chung_chi" : request.files['dinh_kem_chung_chi'],
            # "dinh_kem_anh_chan_dung" : request.files['dinh_kem_anh_chan_dung'],
            # "dinh_kem_xac_nhan_cong_dan" : request.files['dinh_kem_xac_nhan_cong_dan'],
            # "dinh_kem_xac_nhan_khac" : request.files['dinh_kem_xac_nhan_khac'],
        }

        chung_chi_exist = ChungChiHanhNghe.query.filter(ChungChiHanhNghe.nhan_vien_id == current_user.id).first()
        if chung_chi_exist is not None:
            return {"msg": "Dược Sĩ Đã Có Chứng Chỉ Hành Nghề"},  HttpCode.BadRequest

        chung_chi_hanh_nghe = schema.load(req)
        chung_chi_hanh_nghe.nhan_vien_id = current_user.id
        chung_chi_hanh_nghe.created_by = current_user.id

        #         "lan_cap_thu": request.form.get("lan_cap_thu"),
        # "thay_the_chung_chi": request.form.get("thay_the_chung_chi"),
        # "noi_dung_dieu_chinh": request.form.get("noi_dung_dieu_chinh"),

        # if "yeu_cau_phien_dich" in request.form:
        #     yeu_cau_phien_dich = db.func.lower(request.form.get("yeu_cau_phien_dich"))
        #     try :
        #         if yeu_cau_phien_dich == 'true':
        #             chung_chi_hanh_nghe.yeu_cau_phien_dich = True
        #         if yeu_cau_phien_dich == 'false':
        #             chung_chi_hanh_nghe.yeu_cau_phien_dich = False
        #     except:
        #         return {"msg":"Sai Định dạng trạng thái yêu cầu phiên dịch"},  HttpCode.InternalError
        # ! upload file MINIO-SERVER

        chung_chi_hanh_nghe.yeu_cau_phien_dich = True
        if 'dinh_kem_chung_chi' in request.files:
            try:
                dinh_kem_chung_chi = request.files['dinh_kem_chung_chi']
                chung_chi = UploadMinio.upload_duocsi(dinh_kem_chung_chi)
                chung_chi_hanh_nghe.dinh_kem_chung_chi = chung_chi
            except:
                return {"msg": "Tải Đính Kèm Thất Bại"},  HttpCode.InternalError

        if 'dinh_kem_anh_chan_dung' in request.files:
            try:
                dinh_kem_anh_chan_dung = request.files['dinh_kem_anh_chan_dung'],
                anh_chan_dung = UploadMinio.upload_duocsi(dinh_kem_anh_chan_dung)
                chung_chi_hanh_nghe.dinh_kem_anh_chan_dung = anh_chan_dung
            except:
                return {"msg": "Tải Đính Kèm Thất Bại"},  HttpCode.InternalError

        if 'dinh_kem_xac_nhan_cong_dan' in request.files:
            try:
                dinh_kem_xac_nhan_cong_dan = request.files['dinh_kem_xac_nhan_cong_dan'],
                xac_nhan_cong_dan = UploadMinio.upload_duocsi(dinh_kem_xac_nhan_cong_dan)
                chung_chi_hanh_nghe.dinh_kem_xac_nhan_cong_dan = xac_nhan_cong_dan
            except:
                return {"msg": "Tải Đính Kèm Thất Bại"},  HttpCode.InternalError

        if 'dinh_kem_xac_nhan_khac' in request.files:
            try:
                dinh_kem_xac_nhan_khac = request.files['dinh_kem_xac_nhan_khac'],
                xac_nhan_khac = UploadMinio.upload_duocsi(dinh_kem_xac_nhan_khac)
                chung_chi_hanh_nghe.dinh_kem_xac_nhan_khac = xac_nhan_khac
            except:
                return {"msg": "Tải Đính Kèm Thất Bại"},  HttpCode.InternalError

        # try:
        #     dinh_kem_chung_chi = UploadMinio.upload_duocsi(req.get("dinh_kem_chung_chi"))
        #     dinh_kem_anh_chan_dung = UploadMinio.upload_duocsi(req.get("dinh_kem_anh_chan_dung"))
        #     dinh_kem_xac_nhan_cong_dan = UploadMinio.upload_duocsi(req.get("dinh_kem_xac_nhan_cong_dan"))
        #     dinh_kem_xac_nhan_khac = UploadMinio.upload_duocsi(req.get("dinh_kem_xac_nhan_khac"))
        #     chung_chi_hanh_nghe.dinh_kem_chung_chi = dinh_kem_chung_chi
        #     chung_chi_hanh_nghe.dinh_kem_anh_chan_dung = dinh_kem_anh_chan_dung
        #     chung_chi_hanh_nghe.dinh_kem_xac_nhan_cong_dan = dinh_kem_xac_nhan_cong_dan
        #     chung_chi_hanh_nghe.dinh_kem_xac_nhan_khac = dinh_kem_xac_nhan_khac
        # except:
        #     return {"msg":"Tải Đính Kèm Thất Bại"},  HttpCode.InternalError

        # ! relationship
        van_bang_chuyen_mon_id = request.form.get("van_bang_chuyen_mon_id")

        VanBangChuyenMon.query.filter(VanBangChuyenMon.id == van_bang_chuyen_mon_id).first_or_404()

        chung_chi_hanh_nghe.van_bang_chuyen_mon_id = van_bang_chuyen_mon_id

        pham_vi_chuyen_mon_ids = request.form.getlist("pham_vi_chuyen_mon_ids")

        pham_vi_chuyen_mons = PhamViHoatDongChuyenMon.query.filter(
            PhamViHoatDongChuyenMon.id.in_(pham_vi_chuyen_mon_ids)).all()
        for pham_vi_chuyen_mon in pham_vi_chuyen_mons:
            chung_chi_hanh_nghe.pham_vi_chuyen_mon.append(pham_vi_chuyen_mon)

        vi_tri_hanh_nghe_ids = request.form.getlist("vi_tri_hanh_nghe_ids")

        vi_tri_hanh_nghes = ViTriHanhNghe.query.filter(ViTriHanhNghe.id.in_(vi_tri_hanh_nghe_ids)).all()
        for vi_tri_hanh_nghe in vi_tri_hanh_nghes:
            chung_chi_hanh_nghe.vi_tri_hanh_nghe.append(vi_tri_hanh_nghe)

        chung_chi_hanh_nghe.trang_thai_ho_so = "0"
        chung_chi_hanh_nghe.loai_cap_chung_chi = "1"
        chung_chi_hanh_nghe.lan_cap_thu = 1
        db.session.add(chung_chi_hanh_nghe)
        db.session.commit()

        return schema.dump(chung_chi_hanh_nghe), HttpCode.OK


class ChungChiHanhNgheById(Resource):

    @ jwt_required()
    def put(self, id):
        chung_chi_schema = CCHNInfoSchema(partial=True)
        tthc_schema = ThongTinHanhChinhSchema(partial=True)

        data = {
            "thong_tin_hanh_chinh": json.loads(request.form.get("thong_tin_hanh_chinh")),
            "thong_tin_chung_chi": json.loads(request.form.get("thong_tin_chung_chi")),
            "pham_vi_chuyen_mon_ids": request.form.getlist("pham_vi_chuyen_mon_ids[]"),
            "vi_tri_hanh_nghe": request.form.get("vi_tri_hanh_nghe_ids[]"),
            "ghi_chu": request.form.get("ghi_chu"),
            "danh_sach_dinh_kem": []
        }

        chung_chi_hanh_nghe: ChungChiHanhNghe = ChungChiHanhNghe.query.get_or_404(id)
        thong_tin_hanh_chinh = chung_chi_hanh_nghe.nhan_vien

        if data.get("thong_tin_hanh_chinh", None):
            thong_tin_hanh_chinh = tthc_schema.load(data.get("thong_tin_hanh_chinh"), instance=thong_tin_hanh_chinh)
        if data.get("thong_tin_chung_chi", None):
            if data["thong_tin_hanh_chinh"].get("so_giay_phep", None):
                exist = ChungChiHanhNghe.query.join(
                    User, and_(User.id == ChungChiHanhNghe.nhan_vien_id, User.da_cap_chung_chi == True))\
                    .filter(User.tai_khoan_id != None, ChungChiHanhNghe.so_giay_phep.like(data["thong_tin_hanh_chinh"]["so_giay_phep"]))\
                    .options(noload(ChungChiHanhNghe.pham_vi_chuyen_mon),
                             noload(ChungChiHanhNghe.vi_tri_hanh_nghe),
                             noload(ChungChiHanhNghe.van_bang_chuyen_mon)).first()
                if exist:
                    return {
                        "msg": "Số giấy phép đã tồn tại"
                    }, HttpCode.BadRequest
            chung_chi_hanh_nghe = chung_chi_schema.load(data.get("thong_tin_chung_chi"), instance=chung_chi_hanh_nghe)

        if data.get("pham_vi_chuyen_mon_ids[]", []):
            target_pvhd = None
            if len(list(filter(None, data.get("pham_vi_chuyen_mon_ids[]", [])))) > 0:
                target_pvhd = PhamViHoatDongChuyenMon.query.filter(
                    PhamViHoatDongChuyenMon.id.in_(data.get("pham_vi_chuyen_mon_ids[]", []))).all()
            chung_chi_hanh_nghe.pham_vi_chuyen_mon.clear()
            if target_pvhd:
                chung_chi_hanh_nghe.pham_vi_chuyen_mon = target_pvhd
        if data.get("vi_tri_hanh_nghe_ids[]", []):
            target_vthn = None
            if len(list(filter(None, data.get("vi_tri_hanh_nghe_ids[]", [])))) > 0:
                target_vthn = ViTriHanhNghe.query.filter(
                    ViTriHanhNghe.id.in_(data.get("vi_tri_hanh_nghe_ids[]", []))).all()
            chung_chi_hanh_nghe.vi_tri_hanh_nghe.clear()
            if target_vthn:
                chung_chi_hanh_nghe.vi_tri_hanh_nghe = target_vthn

        if data.get("ghi_chu", None):
            if data["ghi_chu"].get("ghi_chu_pham_vi_hoat_dong", None):
                chung_chi_hanh_nghe.ghi_chu_pham_vi_hanh_nghe = data["ghi_chu"]["ghi_chu_pham_vi_hoat_dong"]
            if data["ghi_chu"].get("ghi_chu_vi_tri_hanh_nghe", None):
                chung_chi_hanh_nghe.ghi_chu_vi_tri_hanh_nghe = data["ghi_chu"]["ghi_chu_vi_tri_hanh_nghe"]
            if data["ghi_chu"].get("ghi_chu_chung", None):
                chung_chi_hanh_nghe.ghi_chu = data["ghi_chu"]["ghi_chu_chung"]
        db.session.commit()

        return {"msg": "Cập Nhật Thành Công"},  HttpCode.OK

    def get(self, id):
        res = {
            "thong_tin_hanh_chinh": None,
            "thong_tin_chung_chi": None,
            "pham_vi_chuyen_mon": None,
            "vi_tri_hanh_nghe": None,
            "ghi_chu": None,
            "danh_sach_dinh_kem": None
        }

        schema_pvhd_cm_display = PhamViHoatDongChuyenMonDisplaySchema(many=True)
        schema_pvhd_current = PhamViHoatDongChuyenMonSchema(many=True, only=["id"])
        schema_vt_hn_display = ViTriHanhNgheParentDisplaySchema(many=True)
        schema_vt_hn_current = ViTriHanhNgheSchema(many=True, only=["id"])

        target_cchn: ChungChiHanhNghe = ChungChiHanhNghe.query.filter_by(id=id).first_or_404()
        target_user = target_cchn.nhan_vien
        # Add thong_tin_hanh_chinh data
        res["thong_tin_hanh_chinh"] = ThongTinHanhChinhSchema().dump(target_user)
        res["thong_tin_chung_chi"] = CCHNInfoSchema().dump(target_cchn)
        # data pham_vi_chuyen_mon
        pvhd_chuyen_mon_checked_list = [x["id"] for x in schema_pvhd_current.dump(target_user.chung_chi_hanh_nghe.pham_vi_chuyen_mon)] \
            if target_user.chung_chi_hanh_nghe\
            else None
        if redisdb.exists("danh_sach:pham_vi_hoat_dong_chuyen_mon"):
            danh_sach_pvhd_cm_res = json.loads(redisdb.get("danh_sach:pham_vi_hoat_dong_chuyen_mon"))
        else:
            danh_sach_pvhd = PhamViHoatDongChuyenMon.query.all()
            danh_sach_pvhd_cm_res = schema_pvhd_cm_display.dump(danh_sach_pvhd)
            redisdb.set("danh_sach:pham_vi_hoat_dong_chuyen_mon", schema_pvhd_cm_display.dumps(danh_sach_pvhd))
        res["pham_vi_chuyen_mon"] = {
            "danh_sach": danh_sach_pvhd_cm_res,
            "checked": pvhd_chuyen_mon_checked_list
        }

        # * data vi_tri_hanh_nghe
        vt_nt_checked = [x["id"] for x in schema_vt_hn_current.dump(target_user.chung_chi_hanh_nghe.vi_tri_hanh_nghe)]\
            if target_user.chung_chi_hanh_nghe\
            else None
        if redisdb.exists("danh_sach:vi_tri_hanh_nghe"):
            danh_sach_vt_hn_res = json.loads(redisdb.get("danh_sach:vi_tri_hanh_nghe"))
        else:
            danh_sach_vt_hn = ViTriHanhNghe.query.filter(ViTriHanhNghe.parent_id == None).options(
                joinedload("children")
            ).all()
            danh_sach_vt_hn_res = schema_vt_hn_display.dump(danh_sach_vt_hn)
            redisdb.set("danh_sach:vi_tri_hanh_nghe", schema_vt_hn_display.dumps(danh_sach_vt_hn))

        res["vi_tri_hanh_nghe"] = {
            "danh_sach": danh_sach_vt_hn_res,
            "checked": vt_nt_checked
        }

        res["ghi_chu"] = {
            "ghi_chu_pham_vi_hoat_dong": target_cchn.ghi_chu_pham_vi_hanh_nghe,
            "ghi_chu_vi_tri_hanh_nghe": target_cchn.ghi_chu_vi_tri_hanh_nghe,
            "ghi_chu_chung": target_cchn.ghi_chu
        }
        return {
            "msg": "Thành công",
            "results": res
        }, HttpCode.OK

    def delete(self, id):
        chung_chi_hanh_nghe: ChungChiHanhNghe = ChungChiHanhNghe.query.get_or_404(id)
        db.session.delete(chung_chi_hanh_nghe)
        db.session.commit()
        return {
            "msg": "Xóa thành công"
        }, HttpCode.OK


class ChungChiHanhNgheGetCurrentInfo(Resource):
    @ jwt_required()
    def get(self):
        user: User = User.query.filter(User.id == current_user.id).options(
            joinedload(User.chung_chi_hanh_nghe).options(
                joinedload(ChungChiHanhNghe.pham_vi_chuyen_mon),
                joinedload(ChungChiHanhNghe.vi_tri_hanh_nghe))).first()
        if user is None:
            return {"msg": "Người dùng không tồn tại"}, HttpCode.InternalError

        schema_chung_chi = ChungChiHanhNgheSchema(
            only=["nam_cap", "so_giay_phep", "co_quan_cap", "hinh_thuc_thi", "ngay_hieu_luc", "ngay_cap", "phu_trach_chuyen_mon", "trang_thai_ho_so"])
        schema_nhan_vien = NhanVienSchema(
            only=["ho", "ten", "ngay_sinh", "gioi_tinh", "ma_cong_dan", "ngay_cap", "noi_cap"])
        schema_pvhd_cm_display = PhamViHoatDongChuyenMonDisplaySchema(many=True)
        schema_pvhd_current = PhamViHoatDongChuyenMonSchema(many=True, only=["id"])
        schema_van_bang = VanBangChuyenMonDisplaySchema(many=True)
        schema_vt_hn_display = ViTriHanhNgheParentDisplaySchema(many=True)
        schema_vt_hn_current = ViTriHanhNgheSchema(many=True, only=["id"])
        # * check so_giay_phep
        res = {
            "nhan_vien": None,
            "chung_chi": None,
            "van_bang": None,
            "pvhd_chuyen_mon": None,
            "vi_tri_hanh_nghe": None
        }
        # * data nhan_vien
        res["nhan_vien"]: dict = schema_nhan_vien.dump(user)
        # * data chung_chi_hanh_nghe
        res["chung_chi"] = schema_chung_chi.dump(user.chung_chi_hanh_nghe)\
            if user.chung_chi_hanh_nghe\
            else None
        # * data van_bang_chuyen_mon
        current_van_bang: VanBangChuyenMon = user.chung_chi_hanh_nghe.van_bang_chuyen_mon\
            if user.chung_chi_hanh_nghe and user.chung_chi_hanh_nghe.van_bang_chuyen_mon_id\
            else None
        res["van_bang"] = {
            "danh_sach_van_bang": schema_van_bang.dump([x.van_bang_chuyen_mon for x in user.bang_cap if x.van_bang_chuyen_mon]),
            "current_van_bang": VanBangChuyenMonDisplaySchema().dump(current_van_bang) if current_van_bang else None
        }

        # * data pham_vi_chuyen_mon
        pvhd_chuyen_mon_checked_list = [x["id"] for x in schema_pvhd_current.dump(user.chung_chi_hanh_nghe.pham_vi_chuyen_mon)] \
            if user.chung_chi_hanh_nghe\
            else None
        if redisdb.exists("danh_sach:pham_vi_hoat_dong_chuyen_mon"):
            danh_sach_pvhd_cm_res = json.loads(redisdb.get("danh_sach:pham_vi_hoat_dong_chuyen_mon"))
        else:
            danh_sach_pvhd = PhamViHoatDongChuyenMon.query.all()
            danh_sach_pvhd_cm_res = schema_pvhd_cm_display.dump(danh_sach_pvhd)
            redisdb.set("danh_sach:pham_vi_hoat_dong_chuyen_mon", schema_pvhd_cm_display.dumps(danh_sach_pvhd))
        res["pvhd_chuyen_mon"] = {
            "danh_sach_pvhd_chuyen_mon": danh_sach_pvhd_cm_res,
            "pvhd_chuyen_mon_checked": pvhd_chuyen_mon_checked_list
        }

        # * data vi_tri_hanh_nghe
        vt_nt_checked = [x["id"] for x in schema_vt_hn_current.dump(user.chung_chi_hanh_nghe.vi_tri_hanh_nghe)]\
            if user.chung_chi_hanh_nghe\
            else None
        if redisdb.exists("danh_sach:vi_tri_hanh_nghe"):
            danh_sach_vt_hn_res = json.loads(redisdb.get("danh_sach:vi_tri_hanh_nghe"))
        else:
            danh_sach_vt_hn = ViTriHanhNghe.query.filter(ViTriHanhNghe.parent_id == None).options(
                joinedload("children")
            ).all()
            danh_sach_vt_hn_res = schema_vt_hn_display.dump(danh_sach_vt_hn)
            redisdb.set("danh_sach:vi_tri_hanh_nghe", schema_vt_hn_display.dumps(danh_sach_vt_hn))

        res["vi_tri_hanh_nghe"] = {
            "danh_sach_vt_hn": danh_sach_vt_hn_res,
            "vt_hn_checked": vt_nt_checked
        }

        # * data dinh_kem
        res["dinh_kem"] = {
            "dinh_kem_cchnd": user.chung_chi_hanh_nghe.dinh_kem_chung_chi,
            "dinh_kem_chan_dung": user.chung_chi_hanh_nghe.dinh_kem_anh_chan_dung,
            "dinh_kem_cmnd": user.chung_chi_hanh_nghe.dinh_kem_xac_nhan_cong_dan,
            "dinh_kem_giay_to_khac": user.chung_chi_hanh_nghe.dinh_kem_xac_nhan_khac
        } if user.chung_chi_hanh_nghe else None

        return {
            "msg": "Thành công",
            "results": res
        }, HttpCode.OK


class TimKiemTheoTen(Resource):
    # @jwt_required()
    # def get(self):
    #         schema = ChungChiHanhNgheSchema(many = True)
    #         query = ChungChiHanhNghe.query
    #         if "search_key" in request.args:
    #             searchKey = request.args.get('search_key')
    #             if not searchKey.isspace():
    #                 ho_so = query.filter(ChungChiHanhNghe..like(f"%{clean_string(searchKey)}%"))
    #             return paginate(ho_so, schema), HttpCode.OK
    #         return paginate(ho_so, schema)
    @ jwt_required()
    def get(self):

        user_schema = NhanVienSchema()

        pham_vi_chuyen_mon_schema = PhamViHoatDongChuyenMonSchema(many=True)

        pham_vi_chuyen_mon = PhamViHoatDongChuyenMon.query
        vi_hanh_nghe_schema = ViTriHanhNgheSchema(many=True)

        danh_muc_A = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'A')

        checked_danhmuc = []

        danh_muc_A = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'A')
        danh_muc_B = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'B')
        danh_muc_C = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'C')
        danh_muc_D = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'D')

        return {
            "result": {

                "pham_vi_chuyen_mon": pham_vi_chuyen_mon_schema.dump(pham_vi_chuyen_mon),

                "danh_muc_vi_tri_hanh_nghe": [
                    {
                        "ten": "Chịu trách nhiệm chuyên môn về dược của",
                        "value": vi_hanh_nghe_schema.dump(danh_muc_A),
                    },
                    {
                        "ten": "Phụ trách về bảo đảm chất lượng",
                        "value": vi_hanh_nghe_schema.dump(danh_muc_B),
                    },
                    {
                        "ten": "Chịu trách nhiệm chuyên môn về dược, người phụ trách về bảo đảm chất lượng",
                        "value": vi_hanh_nghe_schema.dump(danh_muc_C),
                    },
                    {
                        "ten": "Phụ trách công tác dược lâm sàng",
                        "value": vi_hanh_nghe_schema.dump(danh_muc_D),
                    },
                ],
                "checked_danh_muc_pham_vi_hn": [
                    {
                        "value": checked_danhmuc,
                    }
                ],


            },


        }, HttpCode.OK


class ChungChiHanhNgheCompare(Resource):

    @ jwt_required()
    def post(self, id):
        schema_chung_chi_cung_cap = ChungChiHanhNgheSchema(
            only=["id", "nhan_vien_id", "nam_cap", "so_giay_phep", "co_quan_cap", "hinh_thuc_thi", "ngay_hieu_luc", "trang_thai_ho_so",
                  "dinh_kem_chung_chi", "dinh_kem_anh_chan_dung", "dinh_kem_xac_nhan_cong_dan", "dinh_kem_xac_nhan_khac"])
        schema_chung_chi_thong_tin = ChungChiHanhNgheSchema(
            only=["id", "nhan_vien_id", "nam_cap", "so_giay_phep", "co_quan_cap", "hinh_thuc_thi", "ngay_hieu_luc", "trang_thai_ho_so"])
        schema_nhan_vien = NhanVienSchema(
            only=["ho_ten", "ngay_sinh", "gioi_tinh", "ma_cong_dan", "ngay_cap", "noi_cap"])
        schema_pham_vi_chuyen_mon = PhamViHoatDongChuyenMonSchema(many=True)
        schema_vi_tri_hanh_nghe = ViTriHanhNgheSchema(many=True)
        # * check so_giay_phep
        diff_list = []

        chung_chi_moi: ChungChiHanhNghe = ChungChiHanhNghe.query.filter(
            ChungChiHanhNghe.id == id, ChungChiHanhNghe.nhan_vien.has(User.tai_khoan_id != None)).first_or_404()

        chung_chi_cu: ChungChiHanhNghe = ChungChiHanhNghe.query.filter(
            ChungChiHanhNghe.so_giay_phep.like(chung_chi_moi.so_giay_phep), ChungChiHanhNghe.nhan_vien.has(User.tai_khoan_id == None)).first()

        res = {"thong_tin_cung_cap": None,
               "thong_tin_chung_chi": None,
               "diff": None}

        nv_moi_data: dict = schema_nhan_vien.dump(chung_chi_moi.nhan_vien)
        cc_moi_data: dict = schema_chung_chi_cung_cap.dump(chung_chi_moi)
        cc_moi_data.update(nv_moi_data)
        cc_moi_data["van_bang"] = chung_chi_moi.van_bang_chuyen_mon.ten if chung_chi_moi.van_bang_chuyen_mon else None
        cc_moi_data["pvhd_chuyen_mon"] = [x["ten"]
                                          for x in schema_pham_vi_chuyen_mon.dump(chung_chi_moi.pham_vi_chuyen_mon)]
        cc_moi_data["vi_tri_hanh_nghe"] = [x["ten"]
                                           for x in schema_vi_tri_hanh_nghe.dump(chung_chi_moi.vi_tri_hanh_nghe)]

        res.update({"thong_tin_cung_cap": cc_moi_data})

        if chung_chi_cu:
            if chung_chi_cu.nhan_vien:
                nv_cu_data: dict = schema_nhan_vien.dump(chung_chi_cu.nhan_vien)
            cc_cu_data: dict = schema_chung_chi_thong_tin.dump(chung_chi_cu)
            cc_cu_data.update(nv_cu_data)
            cc_cu_data["van_bang"] = chung_chi_cu.van_bang_chuyen_mon.ten if chung_chi_cu.van_bang_chuyen_mon else None
            cc_cu_data["pvhd_chuyen_mon"] = [x["ten"]
                                             for x in schema_pham_vi_chuyen_mon.dump(chung_chi_cu.pham_vi_chuyen_mon)]
            cc_cu_data["vi_tri_hanh_nghe"] = [x["ten"]
                                              for x in schema_vi_tri_hanh_nghe.dump(chung_chi_cu.vi_tri_hanh_nghe)]

            for key, value in cc_moi_data.items():
                # * if key doesn't exist, skip
                if key not in cc_cu_data:
                    continue
                if cc_cu_data[key] == value:
                    continue
                diff_list.append(key)

            res.update({"thong_tin_chung_chi": cc_cu_data})
        res.update({"diff": diff_list})

        return {
            "msg": "Thành công",
            "results": res
        }


class ChungChiHanhNgheLienKetResource(Resource):
    @ jwt_required()
    def put(self, id):
        try:
            current_chung_chi: ChungChiHanhNghe = ChungChiHanhNghe.query.filter(
                ChungChiHanhNghe.id == id).first_or_404()
            previous_chung_chi: ChungChiHanhNghe = ChungChiHanhNghe.query.filter(
                ChungChiHanhNghe.trang_thai_ho_so == '1', ChungChiHanhNghe.so_giay_phep.like(current_chung_chi.so_giay_phep), ChungChiHanhNghe.nhan_vien.has(User.tai_khoan_id == None)).first()

            current_chung_chi.trang_thai_ho_so = 2
            previous_chung_chi.trang_thai_ho_so = '2'
            # PUSH NOTIFICATION
            fcm_tokens = redisdb.mget(redisdb.keys(pattern="fcm_token:"+str(current_chung_chi.nhan_vien_id)+":*"))
            tieu_de = f"Thông báo liên kết CCHN"
            noi_dung = f"Tài khoản của bạn đã được liên kết với CCHN vào lúc {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
            thong_bao = ThongBao(tieu_de=tieu_de, noi_dung=noi_dung, nhan_vien_id=current_chung_chi.nhan_vien_id)
            if fcm_tokens and len(fcm_tokens) > 0:
                send_push_notification(tieu_de, noi_dung,
                                       registration_tokens=fcm_tokens, to_all=False)
            db.session.add(thong_bao)
            db.session.commit()
            return {
                "msg": "Liên kết thành công"
            }
        except Exception as e:
            return {
                "msg": "Đã xảy ra lỗi khi liên kết chứng chỉ, vui lòng thử lại sau",
                "error": e.args[0]
            }, HttpCode.BadRequest


class ChungChiHanhNgheTuChoiLienKetResource(Resource):
    @ jwt_required()
    def put(self, id):
        try:
            current_chung_chi: ChungChiHanhNghe = ChungChiHanhNghe.query.filter(
                ChungChiHanhNghe.id == id).first_or_404()
            current_chung_chi.trang_thai_ho_so = '3'
            previous_chung_chi: ChungChiHanhNghe = ChungChiHanhNghe.query.filter(
                ChungChiHanhNghe.so_giay_phep.like(current_chung_chi.so_giay_phep), ChungChiHanhNghe.nhan_vien.has(User.tai_khoan_id == None)).first()
            previous_chung_chi.trang_thai_ho_so = '1'
            # PUSH NOTIFICATION
            fcm_tokens = redisdb.mget(redisdb.keys(pattern="fcm_token:"+str(current_chung_chi.nhan_vien_id)+":*"))
            tieu_de = f"Thông báo liên kết CCHN bị từ chối"
            noi_dung = f"{current_user.ho_ten} đã từ chối yêu cầu liên kết CCHN của bạn vào lúc {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
            thong_bao = ThongBao(tieu_de=tieu_de, noi_dung=noi_dung, nhan_vien_id=current_chung_chi.nhan_vien_id)
            if fcm_tokens and len(fcm_tokens) > 0:
                send_push_notification(tieu_de, noi_dung,
                                       registration_tokens=fcm_tokens, to_all=False)
            db.session.add(thong_bao)
            db.session.commit()
            return {
                "msg": "Từ chối liên kết thành công"
            }
        except Exception as e:
            return {
                "msg": "Đã xảy ra lỗi khi thực hiện lệnh, vui lòng thử lại sau",
                "error": e.args[0]
            }, HttpCode.BadRequest


class ChungChiHanhNgheGetInfo(Resource):
    @ jwt_required()
    def get(self):

        current_chung_chi: ChungChiHanhNghe = current_user.chung_chi_hanh_nghe

        if not current_chung_chi:
            return {
                "msg": "Chứng chỉ không tồn tại",
                "results": None
            }, HttpCode.OK

        res = {
            "msg": "Thành công",
            "results": None
        }

        schema = ChungChiHanhNgheSchema(only=["so_giay_phep", "co_quan_cap", "ngay_hieu_luc",
                                              "van_bang_chuyen_mon.ten", "hinh_thuc_thi", "phu_trach_chuyen_mon", "trang_thai_ho_so"])
        res["results"] = schema.dump(current_chung_chi)
        if current_chung_chi.pham_vi_chuyen_mon and len(current_chung_chi.pham_vi_chuyen_mon) > 0:
            pham_vi_hoat_dong: list[str] = [x.ten for x in current_chung_chi.pham_vi_chuyen_mon]
            pham_vi_hoat_dong = ", ".join(pham_vi_hoat_dong)
            res["results"]["pham_vi_hoat_dong_chuyen_mon"] = pham_vi_hoat_dong
        if current_chung_chi.vi_tri_hanh_nghe and len(current_chung_chi.vi_tri_hanh_nghe) > 0:
            vi_tri_hanh_nghe: list[str] = [x.ten for x in current_chung_chi.vi_tri_hanh_nghe]
            vi_tri_hanh_nghe = ", ".join(vi_tri_hanh_nghe)
            res["results"]["vi_tri_hanh_nghe"] = vi_tri_hanh_nghe
        if current_chung_chi.van_bang_chuyen_mon:
            van_bang_chuyen_mon = current_chung_chi.van_bang_chuyen_mon.ten
            res["results"]["van_bang_chuyen_mon"] = van_bang_chuyen_mon

        return res, HttpCode.OK

    def post(self):
        cc_schema = ChungChiHanhNgheSchema()
        nv_schema = NguoiDungDisplaySchema()

        so_giay_phep = request.json.get("so_giay_phep")

        current_chungchi = ChungChiHanhNghe.query.filter(ChungChiHanhNghe.so_giay_phep == so_giay_phep).first()
        if current_chungchi is not None:
            chung_chi = cc_schema.dump(current_chungchi)
            nhan_vien_id = current_chungchi.nhan_vien_id

            if nhan_vien_id is not None:
                nhan_vien = User.query.filter(User.id == nhan_vien_id).first()
                if nhan_vien is not None:
                    chung_chi["doi_tuong"] = nv_schema.dump(nhan_vien)
            return {"msg": "Thành công", "results": chung_chi}, HttpCode.OK
        else:
            return {"msg": "Chứng chỉ không tồn tại."}, HttpCode.BadRequest


class ChungChiHanhNgheLuuThongTin(Resource):
    @ jwt_required()
    def put(self):
        data = {
            "so_giay_phep": request.form.get("so_giay_phep", None),
            "co_quan_cap": request.form.get("co_quan_cap", None),
            "noi_cap": request.form.get("noi_cap", None),
            "ngay_cap": request.form.get("ngay_cap", None),
            "hinh_thuc_thi": request.form.get("hinh_thuc_thi", None),
            "phu_trach_chuyen_mon": request.form.get("phu_trach_chuyen_mon", None),
            "van_bang_chuyen_mon_id": request.form.get("van_bang_chuyen_mon_id", None),
        }

        current_chung_chi: ChungChiHanhNghe = current_user.chung_chi_hanh_nghe
        if not data.get("so_giay_phep", None):
            return {
                "msg": "Thiếu số giấy phép, vui lòng nhập vào"
            }, HttpCode.BadRequest

        check_existed = ChungChiHanhNghe.query.filter(
            ChungChiHanhNghe.trang_thai_ho_so == '1',
            ChungChiHanhNghe.so_giay_phep.like(data.get("so_giay_phep")),
            ChungChiHanhNghe.nhan_vien.has(User.tai_khoan_id == None)
        ).first()

        if not check_existed:
            return {
                "msg": "Số giấy phép không tồn tại, vui lòng kiểm tra lại"
            }, HttpCode.BadRequest

        if not current_chung_chi:
            current_chung_chi = ChungChiHanhNgheSchema(exclude=["trang_thai_ho_so", "nhan_vien_id"]).load(data)
            current_chung_chi.nhan_vien_id = str(current_user.id)
            db.session.add(current_chung_chi)
            db.session.flush()
        else:
            data["trang_thai_ho_so"] = '0'
            current_chung_chi = ChungChiHanhNgheSchema(partial=True).load(data=data, instance=current_chung_chi)
            db.session.flush()

        if request.form.getlist("pham_vi_chuyen_mon_ids[]", None):
            target_pvhd = None
            if len(list(filter(None, request.form.getlist("pham_vi_chuyen_mon_ids[]")))) > 0:
                target_pvhd = PhamViHoatDongChuyenMon.query.filter(
                    PhamViHoatDongChuyenMon.id.in_(request.form.getlist("pham_vi_chuyen_mon_ids[]"))).all()
            current_chung_chi.pham_vi_chuyen_mon.clear()
            if target_pvhd:
                current_chung_chi.pham_vi_chuyen_mon = target_pvhd

        if request.form.getlist("vi_tri_hanh_nghe_ids[]", None) and len(request.form.getlist("vi_tri_hanh_nghe_ids[]")) > 0:
            current_chung_chi.vi_tri_hanh_nghe.clear()
            target_pvhd = ViTriHanhNghe.query.filter(ViTriHanhNghe.id.in_(
                request.form.getlist("vi_tri_hanh_nghe_ids[]"))).all()
            current_chung_chi.vi_tri_hanh_nghe = target_pvhd

        upload_errors = []
        # * Upload hinh chup CCHND
        danh_sach_hinh_chup_cchnd = request.files.getlist("dinh_kem_hinh_chup_cchnd[]")
        if danh_sach_hinh_chup_cchnd and len(danh_sach_hinh_chup_cchnd) > 0:
            danh_sach_link_cchnd, errors = UploadMinio.upload_duocsi(danh_sach_hinh_chup_cchnd, many=True)
            if current_chung_chi.dinh_kem_chung_chi:
                current_chung_chi.dinh_kem_chung_chi.extend(danh_sach_link_cchnd)
            else:
                current_chung_chi.dinh_kem_chung_chi = danh_sach_link_cchnd
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_hinh_chup_cchnd[]") and current_chung_chi.dinh_kem_chung_chi:
            current_chung_chi.dinh_kem_chung_chi = [
                x for x in current_chung_chi.dinh_kem_chung_chi if x["url"] not in request.form.getlist("delete_dinh_kem_hinh_chup_cchnd[]")]

        # * Upload hinh chup chan dung
        danh_sach_anh_chan_dung = request.files.getlist("dinh_kem_anh_chan_dung[]")
        if danh_sach_anh_chan_dung and len(danh_sach_anh_chan_dung) > 0:
            danh_sach_link_chan_dung, errors = UploadMinio.upload_duocsi(danh_sach_anh_chan_dung, many=True)
            if current_chung_chi.dinh_kem_anh_chan_dung:
                current_chung_chi.dinh_kem_anh_chan_dung.extend(danh_sach_link_chan_dung)
            else:
                current_chung_chi.dinh_kem_anh_chan_dung = danh_sach_link_chan_dung
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_anh_chan_dung[]") and current_chung_chi.dinh_kem_anh_chan_dung:
            current_chung_chi.dinh_kem_anh_chan_dung = [
                x for x in current_chung_chi.dinh_kem_anh_chan_dung if x["url"] not in request.form.getlist("delete_dinh_kem_anh_chan_dung[]")]

        # * Upload hinh chup cmnd
        danh_sach_cmnd = request.files.getlist("dinh_kem_cmnd[]")
        if danh_sach_cmnd and len(danh_sach_cmnd) > 0:
            danh_sach_link_cmnd, errors = UploadMinio.upload_duocsi(danh_sach_cmnd, many=True)
            if current_chung_chi.dinh_kem_xac_nhan_cong_dan:
                current_chung_chi.dinh_kem_xac_nhan_cong_dan.extend(danh_sach_link_cmnd)
            else:
                current_chung_chi.dinh_kem_xac_nhan_cong_dan = danh_sach_link_cmnd
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_cmnd[]") and current_chung_chi.dinh_kem_xac_nhan_cong_dan:
            current_chung_chi.dinh_kem_xac_nhan_cong_dan = [
                x for x in current_chung_chi.dinh_kem_xac_nhan_cong_dan if x["url"] not in request.form.getlist("delete_dinh_kem_cmnd[]")]

        # * Upload hinh chup khac
        danh_sach_khac = request.files.getlist("dinh_kem_khac[]")
        if danh_sach_khac and len(danh_sach_khac) > 0:
            danh_sach_link_khac, errors = UploadMinio.upload_duocsi(danh_sach_khac, many=True)
            if current_chung_chi.dinh_kem_xac_nhan_khac:
                current_chung_chi.dinh_kem_xac_nhan_khac.extend(danh_sach_link_khac)
            else:
                current_chung_chi.dinh_kem_xac_nhan_khac = danh_sach_link_khac
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_khac[]") and current_chung_chi.dinh_kem_xac_nhan_khac:
            current_chung_chi.dinh_kem_xac_nhan_khac = [
                x for x in current_chung_chi.dinh_kem_xac_nhan_khac if x["url"] not in request.form.getlist("delete_dinh_kem_khac[]")]

        db.session.commit()
        return {
            "msg": "Lưu thông tin thành công",
            "upload_errors": upload_errors
        }, HttpCode.OK


class ChungChiHanhNgheGuiYeuCau(Resource):
    @ jwt_required()
    def put(self):
        data = {
            "so_giay_phep": request.form.get("so_giay_phep", None),
            "co_quan_cap": request.form.get("co_quan_cap", None),
            "noi_cap": request.form.get("noi_cap", None),
            "ngay_cap": request.form.get("ngay_cap", None),
            "hinh_thuc_thi": request.form.get("hinh_thuc_thi", None),
            "phu_trach_chuyen_mon": request.form.get("phu_trach_chuyen_mon", None),
            "van_bang_chuyen_mon_id": request.form.get("van_bang_chuyen_mon_id", None),
        }
        current_chung_chi: ChungChiHanhNghe = current_user.chung_chi_hanh_nghe
        if not data.get("so_giay_phep", None):
            return {
                "msg": "Thiếu số giấy phép, vui lòng nhập vào"
            }, HttpCode.BadRequest

        check_existed = ChungChiHanhNghe.query.filter(
            ChungChiHanhNghe.trang_thai_ho_so == '1',
            ChungChiHanhNghe.so_giay_phep.like(data.get("so_giay_phep")),
            ChungChiHanhNghe.nhan_vien.has(User.tai_khoan_id == None)
        ).first()

        if not check_existed:
            return {
                "msg": "Số giấy phép không tồn tại, vui lòng kiểm tra lại"
            }, HttpCode.BadRequest

        if not current_chung_chi:
            current_chung_chi = ChungChiHanhNgheSchema(exclude=["trang_thai_ho_so", "nhan_vien_id"]).load(data)
            current_chung_chi.nhan_vien_id = str(current_user.id)
            current_chung_chi.trang_thai_ho_so = '1'
            current_chung_chi.thoi_gian_yeu_cau_lien_ket = int(datetime.now().timestamp())
            db.session.add(current_chung_chi)
            db.session.flush()
        else:
            data["trang_thai_ho_so"] = '1'
            data["thoi_gian_yeu_cau_lien_ket"] = int(datetime.now().timestamp())
            current_chung_chi = ChungChiHanhNgheSchema(partial=True).load(data=data, instance=current_chung_chi)
            db.session.flush()

        if request.form.getlist("pham_vi_chuyen_mon_ids[]", None):
            target_pvhd = None
            if len(list(filter(None, request.form.getlist("pham_vi_chuyen_mon_ids[]")))) > 0:
                target_pvhd = PhamViHoatDongChuyenMon.query.filter(
                    PhamViHoatDongChuyenMon.id.in_(request.form.getlist("pham_vi_chuyen_mon_ids[]"))).all()
            current_chung_chi.pham_vi_chuyen_mon.clear()
            if target_pvhd:
                current_chung_chi.pham_vi_chuyen_mon = target_pvhd

        if request.form.getlist("vi_tri_hanh_nghe_ids[]", None) and len(request.form.getlist("vi_tri_hanh_nghe_ids[]")) > 0:
            current_chung_chi.vi_tri_hanh_nghe.clear()
            target_pvhd = ViTriHanhNghe.query.filter(ViTriHanhNghe.id.in_(
                request.form.getlist("vi_tri_hanh_nghe_ids[]"))).all()
            current_chung_chi.vi_tri_hanh_nghe = target_pvhd

        upload_errors = []
        # * Upload hinh chup CCHND
        danh_sach_hinh_chup_cchnd = request.files.getlist("dinh_kem_hinh_chup_cchnd[]")
        if danh_sach_hinh_chup_cchnd and len(danh_sach_hinh_chup_cchnd) > 0:
            danh_sach_link_cchnd, errors = UploadMinio.upload_duocsi(danh_sach_hinh_chup_cchnd, many=True)
            if current_chung_chi.dinh_kem_don_de_nghi:
                current_chung_chi.dinh_kem_chung_chi.extend(danh_sach_link_cchnd)
            else:
                current_chung_chi.dinh_kem_chung_chi = danh_sach_link_cchnd
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_hinh_chup_cchnd[]") and current_chung_chi.dinh_kem_chung_chi:
            current_chung_chi.dinh_kem_chung_chi = [
                x for x in current_chung_chi.dinh_kem_chung_chi if x["url"] not in request.form.getlist("delete_dinh_kem_hinh_chup_cchnd[]")]

        # * Upload hinh chup chan dung
        danh_sach_anh_chan_dung = request.files.getlist("dinh_kem_anh_chan_dung[]")
        if danh_sach_anh_chan_dung and len(danh_sach_anh_chan_dung) > 0:
            danh_sach_link_chan_dung, errors = UploadMinio.upload_duocsi(danh_sach_anh_chan_dung, many=True)
            if current_chung_chi.dinh_kem_anh_chan_dung:
                current_chung_chi.dinh_kem_anh_chan_dung.extend(danh_sach_link_chan_dung)
            else:
                current_chung_chi.dinh_kem_anh_chan_dung = danh_sach_link_chan_dung
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_anh_chan_dung[]") and current_chung_chi.dinh_kem_anh_chan_dung:
            current_chung_chi.dinh_kem_anh_chan_dung = [
                x for x in current_chung_chi.dinh_kem_anh_chan_dung if x["url"] not in request.form.getlist("delete_dinh_kem_anh_chan_dung[]")]

        # * Upload hinh chup cmnd
        danh_sach_cmnd = request.files.getlist("dinh_kem_cmnd[]")
        if danh_sach_cmnd and len(danh_sach_cmnd) > 0:
            danh_sach_link_cmnd, errors = UploadMinio.upload_duocsi(danh_sach_cmnd, many=True)
            if current_chung_chi.dinh_kem_xac_nhan_cong_dan:
                current_chung_chi.dinh_kem_xac_nhan_cong_dan.extend(danh_sach_link_cmnd)
            else:
                current_chung_chi.dinh_kem_xac_nhan_cong_dan = danh_sach_link_cmnd
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_cmnd[]") and current_chung_chi.dinh_kem_xac_nhan_cong_dan:
            current_chung_chi.dinh_kem_xac_nhan_cong_dan = [
                x for x in current_chung_chi.dinh_kem_xac_nhan_cong_dan if x["url"] not in request.form.getlist("delete_dinh_kem_cmnd[]")]

        # * Upload hinh chup khac
        danh_sach_khac = request.files.getlist("dinh_kem_khac[]")
        if danh_sach_khac and len(danh_sach_khac) > 0:
            danh_sach_link_khac, errors = UploadMinio.upload_duocsi(danh_sach_khac, many=True)
            if current_chung_chi.dinh_kem_xac_nhan_khac:
                current_chung_chi.dinh_kem_xac_nhan_khac.extend(danh_sach_link_khac)
            else:
                current_chung_chi.dinh_kem_xac_nhan_khac = danh_sach_link_khac
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_khac[]") and current_chung_chi.dinh_kem_xac_nhan_khac:
            current_chung_chi.dinh_kem_xac_nhan_khac = [
                x for x in current_chung_chi.dinh_kem_xac_nhan_khac if x["url"] not in request.form.getlist("delete_dinh_kem_khac[]")]

        db.session.commit()
        return {
            "msg": "Gửi yêu cầu liên kết thành công"
        }, HttpCode.OK


class ChungChiHanhNgheSearchSoGiayPhep(Resource):
    @ jwt_required()
    def get(self):
        so_giay_phep = request.args.get("so_giay_phep")
        chung_chi: ChungChiHanhNghe = ChungChiHanhNghe.query.filter(
            ChungChiHanhNghe.so_giay_phep.like(so_giay_phep),
            ChungChiHanhNghe.trang_thai_ho_so == '2',
            ChungChiHanhNghe.nhan_vien.has(User.tai_khoan_id != None)).first()
        if not chung_chi:
            return {
                "msg": "Chứng chỉ không tồn tại"
            }, HttpCode.BadRequest
        res = {}
        res["nhan_vien"] = NhanVienHanhNgheSchema().dump(chung_chi.nhan_vien)
        res["bang_cap"] = BangCapNguoiHanhNgheSchema().dump(
            chung_chi.nhan_vien.bang_cap) if chung_chi.nhan_vien else None
        res["chung_chi"] = ChungChiHanhNgheSchema(only=["co_quan_cap", "ngay_cap"]).dump(chung_chi)
        res["chung_chi"].update({"ngay_het_han": None})
        if chung_chi.pham_vi_chuyen_mon and len(chung_chi.pham_vi_chuyen_mon) > 0:
            pham_vi_hoat_dong: list[str] = [x.ten for x in chung_chi.pham_vi_chuyen_mon]
            pham_vi_hoat_dong = ", ".join(pham_vi_hoat_dong)
            res["pham_vi_hoat_dong_chuyen_mon"] = pham_vi_hoat_dong
        if chung_chi.vi_tri_hanh_nghe and len(chung_chi.vi_tri_hanh_nghe) > 0:
            vi_tri_hanh_nghe: list[str] = [x.ten for x in chung_chi.vi_tri_hanh_nghe]
            vi_tri_hanh_nghe = ", ".join(vi_tri_hanh_nghe)
            res["vi_tri_hanh_nghe"] = vi_tri_hanh_nghe
        return {
            "msg": "Thành công",
            "results": res
        }, HttpCode.OK
