from datetime import datetime
from application.models import ThongBao
from application.utils.helper.push_notification_helper import send_push_notification
import json
from marshmallow import ValidationError
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from application.commons.pagination import paginate
from application.controllers.auth.helpers import to_dict
from application.controllers.duoc_si import chung_chi_hanh_nghe
from application.models.bang_cap import BangCap
from application.models.chung_chi_hanh_nghe import ChungChiHanhNghe
from application.models.co_so_thuc_hanh import CoSoThucHanh
from application.models.danhmuc_pham_vi_hoat_dong_chuyen_mon import PhamViHoatDongChuyenMon
from application.models.danhmuc_thu_tuc import DanhMucThuTuc
from application.models.danhmuc_vi_tri_hanh_nghe import ViTriHanhNghe
from application.models.lich_su_dao_tao import LichSuDaoTao
from application.models.loai_ma_chung_chi import LOAIMACHUNGCHI
from application.models.tinh_thanh import TinhThanh
from application.models.quan_huyen import QuanHuyen
from application.models.xa_phuong import XaPhuong
from application.models.user import User
from application.models.vai_tro import VaiTro
from application.models.yeu_cau_chung_chi_hanh_nghe import YeuCauChungChiHanhNghe
from application.schemas import yeu_cau_chung_chi_hanh_nghe
from application.schemas.bang_cap import BangCapSchema
from application.schemas import nhan_vien
from application.schemas.chung_chi_hanh_nghe import ChungChiHanhNgheSchema
from application.schemas.co_so_thuc_hanh import CoSoThucHanhSchema
from application.schemas.danhmuc_pham_vi_hoat_dong_chuyen_mon import PhamViHoatDongChuyenMonSchema
from application.schemas.danhmuc_vi_tri_hanh_nghe import ViTriHanhNgheSchema
from application.schemas.dao_tao import DaotaoSchema
from application.schemas.nhan_vien import NhanVienSchema
from application.schemas.yeu_cau_chung_chi_hanh_nghe import YeuCauChungChiHanhNgheGetListPaginateSchema, YeuCauChungChiHanhNgheSchema
from application.utils.helper.convert_timestamp_helper import current_milli_time, plus_time
from application.utils.helper.generate_so_thu_tu import generate_number
from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
from application.utils.validate.uuid_validator import is_valid_uuid
from sqlalchemy import and_
from application.extensions import db, redisdb
from flask import jsonify


# Tao Ho So
class ChungChiHanhNghePost(Resource):

    @jwt_required()
    def post(self):

        schema = YeuCauChungChiHanhNgheSchema()

        req = {
            "thu_tuc_id": request.json.get("thu_tuc_id"),
        }

        try:
            yeu_cau_chung_chi = schema.load(req)
            yeu_cau_chung_chi.nhan_vien_id = current_user.id
            yeu_cau_chung_chi.trang_thai_ho_so = "1"
            yeu_cau_chung_chi.doi_tuong = to_dict(current_user)
            thu_tuc = DanhMucThuTuc.query.filter(DanhMucThuTuc.id == request.json.get("thu_tuc_id")).first()
            if thu_tuc is None:
                return {"errors": "Thủ tục không tồn tại"}, HttpCode.BadRequest
            try:
                if thu_tuc.doi_tuong != '1':
                    return {"errors": "Đối tượng không thuộc thủ tục thực hiện"}, HttpCode.BadRequest
            except:
                return {"errors": "!!!!!!!!!!!"}, HttpCode.InternalError

            if thu_tuc.ma_thu_tuc == 'TT001':
                db.session.add(yeu_cau_chung_chi)
                yeu_cau_chung_chi.lan_cap_thu = '1'
            elif current_user.assigned_role[0].ten_en == "chuyenvien":
                db.session.add(yeu_cau_chung_chi)
            else:
                chung_chi_hanh_nghe: ChungChiHanhNghe = ChungChiHanhNghe.query.filter(
                    ChungChiHanhNghe.nhan_vien_id == current_user.id).first()
                if chung_chi_hanh_nghe:
                    vi_tri_hanh_nghe_ids = [str(x.id) for x in chung_chi_hanh_nghe.vi_tri_hanh_nghe]
                    arr1 = {"id": []}
                    for vi_tri_hanh_nghe in vi_tri_hanh_nghe_ids:
                        arr1["id"].append(vi_tri_hanh_nghe)
                    yeu_cau_chung_chi.vi_tri_hanh_nghe_cchn = arr1

                    pham_vi_chuyen_mon_ids = [str(x.id) for x in chung_chi_hanh_nghe.pham_vi_chuyen_mon]
                    arr2 = {"id": []}
                    for pham_vi_chuyen_mon in pham_vi_chuyen_mon_ids:
                        arr2["id"].append(pham_vi_chuyen_mon)
                    yeu_cau_chung_chi.pham_vi_chuyen_mon = arr2

                    yeu_cau_chung_chi.ngay_cap_cchnd_cu = chung_chi_hanh_nghe.ngay_hieu_luc
                    yeu_cau_chung_chi.thay_the_cchnd = chung_chi_hanh_nghe.so_giay_phep
                    yeu_cau_chung_chi.hinh_thuc = chung_chi_hanh_nghe.hinh_thuc_thi
                    count_yeu_cau_chungchi = YeuCauChungChiHanhNghe.query.filter(
                        YeuCauChungChiHanhNghe.nhan_vien_id == current_user.id, YeuCauChungChiHanhNghe.trang_thai_ho_so == '11').count()
                    yeu_cau_chung_chi.lan_cap_thu = count_yeu_cau_chungchi
                    db.session.add(yeu_cau_chung_chi)
            db.session.commit()

        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest

        return {"msg": "Yêu Cầu chứng chỉ hành nghề tạo thành công", "results": schema.dump(yeu_cau_chung_chi)}, HttpCode.Created

    def put(self):

        schema = YeuCauChungChiHanhNgheSchema()

        req = {
            "thu_tuc_id": request.form.get("thu_tuc_id"),
            "nhan_vien_id": request.form.get("nhan_vien_id"),
        }

        try:
            nhan_vien = User.query.filter(User.id == req["nhan_vien_id"]).first()
            yeu_cau_chung_chi = YeuCauChungChiHanhNghe.query.filter(
                YeuCauChungChiHanhNghe.id == req["thu_tuc_id"]).first()

            if nhan_vien is None:
                return {"msg": "Xảy ra lỗi khi tạo mới người dùng"}, HttpCode.BadRequest
            if yeu_cau_chung_chi is None:
                return {"msg": "Hồ sơ không tồn tại trong hệ thống"}, HttpCode.BadRequest

            yeu_cau_chung_chi.nhan_vien_id = nhan_vien.id
            yeu_cau_chung_chi.doi_tuong = to_dict(nhan_vien)
            count_yeu_cau_chungchi = YeuCauChungChiHanhNghe.query.filter(
                YeuCauChungChiHanhNghe.nhan_vien_id == nhan_vien.id, YeuCauChungChiHanhNghe.trang_thai_ho_so == '11').count()
            yeu_cau_chung_chi.lan_cap_thu = count_yeu_cau_chungchi

            db.session.commit()

        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest
        return {"msg": "Cập nhật thông tin yêu cầu chứng chỉ thành công", "results": schema.dump(yeu_cau_chung_chi)}, HttpCode.Created


# Duoc Si - Update ho so
class YeuCauChungChiHanhNgheById(Resource):
    @jwt_required()
    def put(self, id):

        schema = YeuCauChungChiHanhNgheSchema(partial=True)

        chung_chi = YeuCauChungChiHanhNghe.query.filter(YeuCauChungChiHanhNghe.id == id).first()

        if chung_chi is None:
            return {"msg": "Chứng Chỉ Không Tồn Tại"}, HttpCode.BadRequest

        check_thutuc = DanhMucThuTuc.query.filter(DanhMucThuTuc.id == chung_chi.thu_tuc_id).first()

        if check_thutuc.doi_tuong != '1':
            return {"msg": "Không thuộc đối tượng thực hiện thủ tục"}, HttpCode.BadRequest

        if check_thutuc.trang_thai == True:

            req = {
                "loai_cap_chung_chi": request.form.get("loai_cap_chung_chi"),
                "hinh_thuc": request.form.get("hinh_thuc"),
            }

            chung_chi: YeuCauChungChiHanhNghe = schema.load(req, instance=chung_chi)

            trang_thai_ho_so = request.form.get("trang_thai_ho_so")

            if trang_thai_ho_so == '2':
                thoi_gian_nop_ho_so = current_milli_time()
                thoi_gian_het_han_ho_so = plus_time(30)
                chung_chi.thoi_gian_nop_ho_so = thoi_gian_nop_ho_so
                chung_chi.ngay_het_han_ho_so = thoi_gian_het_han_ho_so
                chung_chi.trang_thai_ho_so = trang_thai_ho_so

            chung_chi.updated_at = db.func.current_timestamp()

            vi_tri_hanh_nghe_ids = request.form.getlist("vi_tri_hanh_nghe_ids")

            vi_tri_hanh_nghe_list = ViTriHanhNghe.query.filter(ViTriHanhNghe.id.in_(vi_tri_hanh_nghe_ids)).all()
            arr = {"id": []}
            for vi_tri_hanh_nghe in vi_tri_hanh_nghe_list:
                arr["id"].append(str(vi_tri_hanh_nghe.id))

            chung_chi.vi_tri_hanh_nghe_cchn = arr
            #     vitri_hanhnghe = vi_tri_hanh_nghe.id
            #     arr.append(vitri_hanhnghe)

            # chung_chi.vi_tri_hanh_nghe_cchn = to_dict(arr)

            upload_errors = []

            # * Upload hinh chup don de nghi
            upload_images(images=request.files.getlist("dinh_kem_don_de_nghi[]"),
                          target_list=chung_chi.dinh_kem_don_de_nghi,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_don_de_nghi[]"),
                          target_list=chung_chi.dinh_kem_don_de_nghi)

            # * Upload hinh chup anh chan dung
            upload_images(images=request.files.getlist("dinh_kem_anh_chan_dung[]"),
                          target_list=chung_chi.dinh_kem_anh_chan_dung,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_anh_chan_dung[]"),
                          target_list=chung_chi.dinh_kem_anh_chan_dung)

            # * Upload hinh chup van bang chuyen mon
            upload_images(images=request.files.getlist("dinh_kem_van_bang_chuyen_mon[]"),
                          target_list=chung_chi.dinh_kem_van_bang_chuyen_mon,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_van_bang_chuyen_mon[]"),
                          target_list=chung_chi.dinh_kem_van_bang_chuyen_mon)

            # * Upload hinh chup xac nhan suc khoe
            upload_images(images=request.files.getlist("dinh_kem_xac_nhan_suc_khoe[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_suc_khoe,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_xac_nhan_suc_khoe[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_suc_khoe)

            # * Upload hinh chup xac nhan thuc hanh
            upload_images(images=request.files.getlist("dinh_kem_xac_nhan_thuc_hanh[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_thuc_hanh,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_xac_nhan_thuc_hanh[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_thuc_hanh)

            # * Upload hinh chup xac nhan dao tao
            upload_images(images=request.files.getlist("dinh_kem_xac_nhan_dao_tao[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_dao_tao,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_xac_nhan_dao_tao[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_dao_tao)

            # * Upload hinh chup xac nhan cong dan
            upload_images(images=request.files.getlist("dinh_kem_xac_nhan_cong_dan[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_cong_dan,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_xac_nhan_cong_dan[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_cong_dan)

            # * Upload hinh chup xac nhan ly lich
            upload_images(images=request.files.getlist("dinh_kem_xac_nhan_ly_lich[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_ly_lich,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_xac_nhan_ly_lich[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_ly_lich)

            # * Upload hinh chup xac nhan le phi
            upload_images(images=request.files.getlist("dinh_kem_xac_nhan_le_phi[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_le_phi,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_xac_nhan_le_phi[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_le_phi)

            # * Upload hinh chup xac nhan le phi
            upload_images(images=request.files.getlist("dinh_kem_xac_nhan_files[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_files,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_xac_nhan_files[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_files)

        if check_thutuc.trang_thai == False and check_thutuc.ma_thu_tuc == 'TT002':

            req = {
                "noi_dung_dieu_chinh": request.form.get("noi_dung_dieu_chinh"),
            }

            chung_chi = schema.load(req, instance=chung_chi)

            trang_thai_ho_so = request.form.get("trang_thai_ho_so")
            if trang_thai_ho_so == '2':
                thoi_gian_nop_ho_so = current_milli_time()
                thoi_gian_het_han_ho_so = plus_time(15)
                chung_chi.thoi_gian_nop_ho_so = thoi_gian_nop_ho_so
                chung_chi.ngay_het_han_ho_so = thoi_gian_het_han_ho_so
                chung_chi.trang_thai_ho_so = trang_thai_ho_so

            chung_chi.updated_at = db.func.current_timestamp()

            upload_errors = []

            upload_images(images=request.files.getlist("dinh_kem_don_de_nghi[]"),
                          target_list=chung_chi.dinh_kem_don_de_nghi,
                          error_list=upload_errors)

            remove_images(target_urls=request.form.get("delete_dinh_kem_don_de_nghi[]"),
                          target_list=chung_chi.dinh_kem_don_de_nghi)

            # * Upload hinh chup anh chan dung
            upload_images(images=request.files.getlist("dinh_kem_anh_chan_dung[]"),
                          target_list=chung_chi.dinh_kem_anh_chan_dung,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_anh_chan_dung[]"),
                          target_list=chung_chi.dinh_kem_anh_chan_dung)

            # * Upload hinh chup xac nhan thay doi
            upload_images(images=request.files.getlist("dinh_kem_xac_nhan_thay_doi[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_thay_doi,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_xac_nhan_thay_doi[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_thay_doi)

            # * Upload hinh chup dinh kem chung chi
            upload_images(images=request.files.getlist("dinh_kem_chung_chi[]"),
                          target_list=chung_chi.dinh_kem_chung_chi,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_chung_chi[]"),
                          target_list=chung_chi.dinh_kem_chung_chi)

            # * Upload hinh chup xac nhan files
            upload_images(images=request.files.getlist("dinh_kem_xac_nhan_files[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_files,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_xac_nhan_files[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_files)

        if check_thutuc.trang_thai == False and check_thutuc.ma_thu_tuc == 'TT003':

            req = {
                "ly_do_mat_hong": request.form.get("ly_do_mat_hong"),
                "confirm": request.form.get("confirm")
            }

            chung_chi = schema.load(req, instance=chung_chi)

            trang_thai_ho_so = request.form.get("trang_thai_ho_so")
            if trang_thai_ho_so == '2':
                thoi_gian_nop_ho_so = current_milli_time()
                thoi_gian_het_han_ho_so = plus_time(15)
                chung_chi.thoi_gian_nop_ho_so = thoi_gian_nop_ho_so
                chung_chi.ngay_het_han_ho_so = thoi_gian_het_han_ho_so
                chung_chi.trang_thai_ho_so = trang_thai_ho_so

            chung_chi.updated_at = db.func.current_timestamp()

            upload_errors = []

            upload_images(images=request.files.getlist("dinh_kem_don_de_nghi[]"),
                          target_list=chung_chi.dinh_kem_don_de_nghi,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_don_de_nghi[]"),
                          target_list=chung_chi.dinh_kem_don_de_nghi)

            # * Upload hinh chup anh chan dung
            upload_images(images=request.files.getlist("dinh_kem_anh_chan_dung[]"),
                          target_list=chung_chi.dinh_kem_anh_chan_dung,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_anh_chan_dung[]"),
                          target_list=chung_chi.dinh_kem_anh_chan_dung)

            # * Upload hinh chup dinh kem chung chi
            upload_images(images=request.files.getlist("dinh_kem_chung_chi[]"),
                          target_list=chung_chi.dinh_kem_chung_chi,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_chung_chi[]"),
                          target_list=chung_chi.dinh_kem_chung_chi)

            # * Upload hinh chup xac nhan files
            upload_images(images=request.files.getlist("dinh_kem_xac_nhan_files[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_files,
                          error_list=upload_errors)
            remove_images(target_urls=request.form.get("delete_dinh_kem_xac_nhan_files[]"),
                          target_list=chung_chi.dinh_kem_xac_nhan_files)

        db.session.commit()
        return {"msg": "Yêu Cầu chứng chỉ hành nghề Gửi Thành Công", "results": schema.dump(chung_chi)}, HttpCode.Created


# Duoc Si - Get detail

    @jwt_required()
    def get(self, id):

        user_schema = NhanVienSchema()
        yeucau_schema = YeuCauChungChiHanhNgheSchema()
        chungchi_schema = ChungChiHanhNgheSchema()

        user = User.query.filter(User.id == current_user.id).first()
        yeu_cau_chung_chi = YeuCauChungChiHanhNghe.query.filter(YeuCauChungChiHanhNghe.id == id).first()
        chung_chi_hanh_nghe = ChungChiHanhNghe.query.filter(
            ChungChiHanhNghe.nhan_vien_id == "af000f84-e51c-4dfc-80cf-04b06a5530dc").first()

        if yeu_cau_chung_chi is None:
            return {"msg": "Don Yeu Cau Chứng Chỉ Không Tồn Tại"}, HttpCode.NotFound

        check_thutuc = DanhMucThuTuc.query.filter(DanhMucThuTuc.id == yeu_cau_chung_chi.thu_tuc_id).first()

        if check_thutuc.ma_thu_tuc == 'TT001':

            vi_hanh_nghe_schema = ViTriHanhNgheSchema(many=True)

            danh_muc_A = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'A')

            danh_muc_B = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'B')
            danh_muc_C = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'C')
            danh_muc_D = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'D')

            loai_de_nghi = json.load(open('application/jsonFile/loai_cap_chung_chi.json', encoding='utf-8'))
            hinh_thuc_thi = json.load(open('application/jsonFile/hinh_thuc_thi.json', encoding='utf-8'))

            return {
                "result": {
                    "thu_tuc": {
                        "ten": check_thutuc.ten,
                        "loai": "1",
                        "doi_tuong": check_thutuc.doi_tuong,
                    },
                    "user": user_schema.dump(user),
                    "de_nghi":
                        {
                            "loai_de_nghi": loai_de_nghi,
                            "hinh_thuc_thi": hinh_thuc_thi,
                            "danh_muc_pham_vi_hn": [
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
                    },
                    "checked_denghi":
                        {
                            "loai_de_nghi": yeu_cau_chung_chi.loai_cap_chung_chi,
                            "hinh_thuc_thi": yeu_cau_chung_chi.hinh_thuc,
                            "danh_muc_pham_vi_hn": yeu_cau_chung_chi.vi_tri_hanh_nghe_cchn
                    },
                    "yeu_cau_cchnd": yeucau_schema.dump(yeu_cau_chung_chi)
                }
            }, HttpCode.OK

        if check_thutuc.ma_thu_tuc == 'TT002':

            return {
                "result": {
                    "thu_tuc": {
                        "ten": check_thutuc.ten + "(Do thay đổi phạm vi hành nghề, hình thức cấp CCHND, hoặc thông tin của người hành nghề như Số chứng minh nhân dân, địa chỉ thường trú,…)",
                        "loai": "2",
                        "doi_tuong": check_thutuc.doi_tuong,
                    },
                    "user": user_schema.dump(user),
                    "noi_dung_dieu_chinh": yeu_cau_chung_chi.noi_dung_dieu_chinh,
                    "yeu_cau_cchnd": yeucau_schema.dump(yeu_cau_chung_chi),
                    "chung_chi_hanh_nghe": chungchi_schema.dump(chung_chi_hanh_nghe)
                }
            }, HttpCode.OK
        # return {"errors": "ERRORS"},  HttpCode.InternalError

        if check_thutuc.ma_thu_tuc == 'TT003':

            return {
                "result": {
                    "thu_tuc": {
                        "ten": check_thutuc.ten,
                        "loai": "3",
                        "doi_tuong": check_thutuc.doi_tuong,
                    },
                    "user": user_schema.dump(user),
                    "ly_do_tu_choi": yeu_cau_chung_chi.ly_do_mat_hong,
                    "yeu_cau_cchnd": yeucau_schema.dump(yeu_cau_chung_chi),
                    "chung_chi_hanh_nghe": chungchi_schema.dump(chung_chi_hanh_nghe)
                }
            }, HttpCode.OK
        return {"errors": "ERRORS"},  HttpCode.InternalError

# Duoc Si - Toan Bo Ho So ById


class YeuCauChungChiGetListById(Resource):
    @jwt_required()
    def post(self):
        schema = YeuCauChungChiHanhNgheGetListPaginateSchema(many=True)
        target_yeu_cau_chung_chi_hanh_nghe: YeuCauChungChiHanhNghe = YeuCauChungChiHanhNghe.query.filter(
            YeuCauChungChiHanhNghe.nhan_vien_id == current_user.id).order_by(YeuCauChungChiHanhNghe.ma_ho_so.desc())
        return paginate(target_yeu_cau_chung_chi_hanh_nghe, schema)


# Get All Ho So
class YeuCauChungChiGetListAll(Resource):
    @jwt_required()
    def post(self):
        schema = YeuCauChungChiHanhNgheGetListPaginateSchema(many=True)
        query = YeuCauChungChiHanhNghe.query.filter(YeuCauChungChiHanhNghe.trang_thai_ho_so != '1')

        ma_ho_so = request.json.get("ma_ho_so", None) or None

        ho_ten = request.json.get("ho_ten", None) or None

        nop_tu = request.json.get("nop_tu", None) or None

        nop_den = request.json.get("nop_den", None) or None

        han_tu = request.json.get("han_tu", None) or None

        han_den = request.json.get("han_den", None) or None

        thu_tuc_id = request.json.get("thu_tuc_id", None) or None

        trang_thai = request.json.get("trang_thai", None) or None

        trang_thai_het_han = request.json.get("trang_thai_het_han", None) or None

        if ma_ho_so is not None:

            query = query.filter(YeuCauChungChiHanhNghe.ma_ho_so.like(f"%{ma_ho_so}%"))

        if ho_ten is not None:

            # query = query.filter(YeuCauChungChiHanhNghe.duoc_si.ten_khong_dau.like(f"%{clean_string(ho_ten)}%"))

            # query = query.options(contains_eager())

            query = query\
                .join(YeuCauChungChiHanhNghe.duoc_si)\
                .filter(User.ten_khong_dau.like(f"%{clean_string(ho_ten)}%"))\

        if nop_tu is not None:
            query = query.filter(YeuCauChungChiHanhNghe.thoi_gian_nop_ho_so >= nop_tu)

        if nop_den is not None:
            query = query.filter(YeuCauChungChiHanhNghe.thoi_gian_nop_ho_so <= nop_den)

        if han_tu is not None:
            query = query.filter(YeuCauChungChiHanhNghe.thoi_gian_nop_ho_so >= han_tu)

        if han_den is not None:
            query = query.filter(YeuCauChungChiHanhNghe.thoi_gian_nop_ho_so <= han_den)

        if thu_tuc_id is not None:

            query = query.filter(str(YeuCauChungChiHanhNghe.thu_tuc_id) == str(thu_tuc_id))

        if trang_thai is not None:

            query = query.filter(YeuCauChungChiHanhNghe.trang_thai_ho_so == trang_thai)

        if trang_thai_het_han is not None and trang_thai_het_han == '1':
            query = query.filter(YeuCauChungChiHanhNghe.trang_thai_het_han == True)
        if trang_thai_het_han is not None and trang_thai_het_han == '2':
            query = query.filter(YeuCauChungChiHanhNghe.trang_thai_het_han == False)
            # .like(f"%{clean_string(searchKey)}%")

        query = query.order_by(YeuCauChungChiHanhNghe.ma_ho_so.desc())

        return paginate(query, schema)


# View Detail Ho So
class YeuCauChungChiGetDetailInList(Resource):
    @jwt_required()
    def get(self, id):
        yeu_cau_chung_chi_schema = YeuCauChungChiHanhNgheSchema()
        yeu_cau_chung_chi = YeuCauChungChiHanhNghe.query.filter(YeuCauChungChiHanhNghe.id == id).first()
        if yeu_cau_chung_chi is None:
            return {"msg": "Hồ Sơ không tồn tại"}, HttpCode.BadRequest

        user = User.query.filter(User.id == yeu_cau_chung_chi.nhan_vien_id).first()

        if user is None:
            return HttpCode.BadRequest

        check_thu_tuc = DanhMucThuTuc.query.filter(DanhMucThuTuc.id == yeu_cau_chung_chi.thu_tuc_id).first()

        if check_thu_tuc.doi_tuong != '1':

            return {"msg": "Không thuộc đối tượng thực hiện"}, HttpCode.BadRequest

        danhmuc_A = []
        danhmuc_B = []
        danhmuc_C = []
        danhmuc_D = []
        b = yeu_cau_chung_chi.vi_tri_hanh_nghe_cchn["id"]
        vi_tri_hinh_nghe_list = ViTriHanhNghe.query.filter(ViTriHanhNghe.id.in_(b)).all()
        for danhmuc in vi_tri_hinh_nghe_list:

            if danhmuc.loai == 'A':
                danhmuc_A.append(danhmuc.rut_gon)

            elif danhmuc.loai == 'B':
                danhmuc_B.append(danhmuc.rut_gon)

            elif danhmuc.loai == 'C':
                danhmuc_C.append(danhmuc.rut_gon)

            elif danhmuc.loai == 'D':
                danhmuc_D.append(danhmuc.rut_gon)

        user_schema = NhanVienSchema()
        vi_tri_hanh_nghe_schema = ViTriHanhNgheSchema(many=True)
        pham_vi_chuyen_mon_schema = PhamViHoatDongChuyenMonSchema(many=True)

        pham_vi_chuyen_mon = PhamViHoatDongChuyenMon.query

        danh_muc_A = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'A')
        danh_muc_B = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'B')
        danh_muc_C = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'C')
        danh_muc_D = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'D')

        if check_thu_tuc.ma_thu_tuc == "TT001":

            return {
                "result": {
                    "thu_tuc": {
                        "ten": check_thu_tuc.ten,
                        "loai": "1",
                                "doi_tuong": check_thu_tuc.doi_tuong,
                    },
                    "user": user_schema.dump(user),
                    "trang_thai_ho_so": yeu_cau_chung_chi.trang_thai_ho_so,
                    "danh_muc_vi_tri_hanh_nghe": [
                        {
                            "ten": "Chịu trách nhiệm chuyên môn về dược của",
                            "value": vi_tri_hanh_nghe_schema.dump(danh_muc_A),
                        },
                        {
                            "ten": "Phụ trách về bảo đảm chất lượng",
                            "value": vi_tri_hanh_nghe_schema.dump(danh_muc_B),
                        },
                        {
                            "ten": "Chịu trách nhiệm chuyên môn về dược, người phụ trách về bảo đảm chất lượng",
                            "value": vi_tri_hanh_nghe_schema.dump(danh_muc_C),
                        },
                        {
                            "ten": "Phụ trách công tác dược lâm sàng",
                            "value": vi_tri_hanh_nghe_schema.dump(danh_muc_D),
                        },
                    ],
                    "danh_muc_pham_vi_chuyen_mon": pham_vi_chuyen_mon_schema.dump(pham_vi_chuyen_mon),
                    "yeu_cau_cchnd": yeu_cau_chung_chi_schema.dump(yeu_cau_chung_chi),
                    "de_nghi":
                    {
                        "loai_de_nghi": yeu_cau_chung_chi.loai_cap_chung_chi,
                        "hinh_thuc_thi": yeu_cau_chung_chi.hinh_thuc,
                        "danh_muc_pham_vi_hn": [
                            {
                                "ten": "Chịu trách nhiệm chuyên môn về dược của",
                                "value": ','.join(danhmuc_A),
                            },
                            {
                                "ten": "Phụ trách về bảo đảm chất lượng",
                                "value": ','.join(danhmuc_B),
                            },
                            {
                                "ten": "Chịu trách nhiệm chuyên môn về dược, người phụ trách về bảo đảm chất lượng",
                                "value": ','.join(danhmuc_C),
                            },
                            {
                                "ten": "Phụ trách công tác dược lâm sàng",
                                "value": ','.join(danhmuc_D),
                            },
                        ],
                    },
                }
            }, HttpCode.OK

        if check_thu_tuc.ma_thu_tuc == "TT002":

            return {
                "result": {
                    "thu_tuc": {
                        "ten": check_thu_tuc.ten,
                        "doi_tuong": check_thu_tuc.doi_tuong,

                    },
                    "user": user_schema.dump(user),
                    "trang_thai_ho_so": yeu_cau_chung_chi.trang_thai_ho_so,
                    "danh_muc_vi_tri_hanh_nghe": [
                        {
                            "ten": "Chịu trách nhiệm chuyên môn về dược của",
                            "value": vi_tri_hanh_nghe_schema.dump(danh_muc_A),
                        },
                        {
                            "ten": "Phụ trách về bảo đảm chất lượng",
                            "value": vi_tri_hanh_nghe_schema.dump(danh_muc_B),
                        },
                        {
                            "ten": "Chịu trách nhiệm chuyên môn về dược, người phụ trách về bảo đảm chất lượng",
                            "value": vi_tri_hanh_nghe_schema.dump(danh_muc_C),
                        },
                        {
                            "ten": "Phụ trách công tác dược lâm sàng",
                            "value": vi_tri_hanh_nghe_schema.dump(danh_muc_D),
                        },
                    ],
                    "danh_muc_pham_vi_chuyen_mon": pham_vi_chuyen_mon_schema.dump(pham_vi_chuyen_mon),
                    "yeu_cau_cchnd": yeu_cau_chung_chi_schema.dump(yeu_cau_chung_chi),
                    "de_nghi":
                    {
                        "loai_de_nghi": yeu_cau_chung_chi.loai_cap_chung_chi,
                        "hinh_thuc_thi": yeu_cau_chung_chi.hinh_thuc,
                        "danh_muc_pham_vi_hn": [
                            {
                                "ten": "Chịu trách nhiệm chuyên môn về dược của",
                                "value": ','.join(danhmuc_A),
                            },
                            {
                                "ten": "Phụ trách về bảo đảm chất lượng",
                                "value": ','.join(danhmuc_B),
                            },
                            {
                                "ten": "Chịu trách nhiệm chuyên môn về dược, người phụ trách về bảo đảm chất lượng",
                                "value": ','.join(danhmuc_C),
                            },
                            {
                                "ten": "Phụ trách công tác dược lâm sàng",
                                "value": ','.join(danhmuc_D),
                            },
                        ],
                    },
                    "noi_dung_xin_dieu_chinh": yeu_cau_chung_chi.noi_dung_dieu_chinh
                }
            }, HttpCode.OK
        if check_thu_tuc.ma_thu_tuc == "TT003":

            return {
                "result": {
                    "thu_tuc": {
                        "ten": check_thu_tuc.ten
                    },
                    "user": user_schema.dump(user),
                    "trang_thai_ho_so": yeu_cau_chung_chi.trang_thai_ho_so,
                    "danh_muc_vi_tri_hanh_nghe": [
                        {
                            "ten": "Chịu trách nhiệm chuyên môn về dược của",
                            "value": vi_tri_hanh_nghe_schema.dump(danh_muc_A),
                        },
                        {
                            "ten": "Phụ trách về bảo đảm chất lượng",
                            "value": vi_tri_hanh_nghe_schema.dump(danh_muc_B),
                        },
                        {
                            "ten": "Chịu trách nhiệm chuyên môn về dược, người phụ trách về bảo đảm chất lượng",
                            "value": vi_tri_hanh_nghe_schema.dump(danh_muc_C),
                        },
                        {
                            "ten": "Phụ trách công tác dược lâm sàng",
                            "value": vi_tri_hanh_nghe_schema.dump(danh_muc_D),
                        },
                    ],
                    "danh_muc_pham_vi_chuyen_mon": pham_vi_chuyen_mon_schema.dump(pham_vi_chuyen_mon),
                    "yeu_cau_cchnd": yeu_cau_chung_chi_schema.dump(yeu_cau_chung_chi),
                    "de_nghi":
                    {
                        "loai_de_nghi": yeu_cau_chung_chi.loai_cap_chung_chi,
                        "hinh_thuc_thi": yeu_cau_chung_chi.hinh_thuc,
                        "danh_muc_pham_vi_hn": [
                            {
                                "ten": "Chịu trách nhiệm chuyên môn về dược của",
                                "value": ','.join(danhmuc_A),
                            },
                            {
                                "ten": "Phụ trách về bảo đảm chất lượng",
                                "value": ','.join(danhmuc_B),
                            },
                            {
                                "ten": "Chịu trách nhiệm chuyên môn về dược, người phụ trách về bảo đảm chất lượng",
                                "value": ','.join(danhmuc_C),
                            },
                            {
                                "ten": "Phụ trách công tác dược lâm sàng",
                                "value": ','.join(danhmuc_D),
                            },
                        ],
                    },
                    "ly_do_mat_hong": yeu_cau_chung_chi.ly_do_mat_hong
                }
            }, HttpCode.OK

        return {"msg": "Internal Server Error "}, HttpCode.InternalError

# Update Ho So Cho Thu Ly


class YeuChungChiThuLy(Resource):
    @jwt_required()
    def post(self):

        user = User.query.filter(User.id == current_user.id).first()
        user.assigned_role

        if "chuyenvien" not in [x.ten_en for x in user.assigned_role]:
            return {"msg": "Người Dùng không có vai trò thụ lý hồ sơ"}, HttpCode.PermissionDenied

        id = request.json.get("id")

        trang_thai_ho_so = request.json.get("trang_thai_ho_so")

        yeu_cau_cchnd: YeuCauChungChiHanhNghe = YeuCauChungChiHanhNghe.query.filter(
            YeuCauChungChiHanhNghe.id == id).first()
        check_thu_tuc = DanhMucThuTuc.query.filter(DanhMucThuTuc.id == yeu_cau_cchnd.thu_tuc_id).first()
        if check_thu_tuc.ma_thu_tuc == 'TT001':
            yeu_cau_cchnd.lan_cap_thu = 1
        else:
            count_yeu_cau = YeuCauChungChiHanhNghe.query.filter(
                YeuCauChungChiHanhNghe.id == yeu_cau_cchnd.id, YeuCauChungChiHanhNghe.thu_tuc_id == yeu_cau_cchnd.thu_tuc_id).all()
            yeu_cau_cchnd.lan_cap_thu = len(count_yeu_cau)
        if yeu_cau_cchnd is None:
            return {"msg": "Yêu Cầu không tồn tại"}, HttpCode.BadRequest

        if yeu_cau_cchnd.trang_thai_het_han == False:

            return {"msg": "Yêu Cầu không thể thực hiện "}, HttpCode.BadRequest

        if trang_thai_ho_so == '4':
            yeu_cau_cchnd.trang_thai_ho_so = trang_thai_ho_so
            yeu_cau_cchnd.nhan_vien_thu_ly_id = current_user.id
            yeu_cau_cchnd.thoi_gian_thu_ly = int(datetime.now().timestamp())
            fcm_tokens = redisdb.mget(redisdb.keys(pattern="fcm_token:"+str(yeu_cau_cchnd.nhan_vien_id)+":*"))
            tieu_de = f"Thụ lý hồ sơ"
            noi_dung = f"Hồ sơ {yeu_cau_cchnd.ma_ho_so} của bạn đã được duyệt vào lúc {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
            thong_bao = ThongBao(tieu_de=tieu_de, noi_dung=noi_dung, nhan_vien_id=yeu_cau_cchnd.nhan_vien_id, dinh_kem={
                                 "yeu_cau_cchnd_id": str(yeu_cau_cchnd.id)})
            db.session.add(thong_bao)

            if fcm_tokens and len(fcm_tokens) > 0:
                send_push_notification(tieu_de, noi_dung,
                                       registration_tokens=fcm_tokens, to_all=False)
            db.session.commit()
            return {"msg": "Thụ Lý Hồ Sơ Thành Công"}, HttpCode.OK

        if trang_thai_ho_so == '3':
            ly_do_tu_choi = request.json.get("ly_do_tu_choi")
            if ly_do_tu_choi is None or "":
                return {"msg": "Vui lòng nhập lý do từ chối"}, HttpCode.BadRequest

            yeu_cau_cchnd.trang_thai_ho_so = trang_thai_ho_so
            yeu_cau_cchnd.ly_do_tu_choi_chuyen_vien = ly_do_tu_choi
            db.session.commit()
            return {"msg": "Từ Chối Hồ Sơ Thành Công"}, HttpCode.OK

        return {"msg": "Internal Server Error "}, HttpCode.InternalError


# Update Trang Thai Ho So


class TrangThaiHoSo(Resource):
    @jwt_required()
    def put(self, id):
        yeu_cau_chung_chi = YeuCauChungChiHanhNghe.query.filter(YeuCauChungChiHanhNghe.id == id).first()
        if yeu_cau_chung_chi is None:
            return {"msg": "Hồ Sơ không tồn tại"}, HttpCode.BadRequest

        trang_thai_ho_so = request.json.get("trang_thai_ho_so")
        noi_dung_tham_xet = request.json.get("noi_dung_tham_xet")
        noi_dung_yeu_cau_bo_sung = request.json.get("noi_dung_yeu_cau_bo_sung")

        yeu_cau_chung_chi.trang_thai_ho_so = trang_thai_ho_so
        yeu_cau_chung_chi.noi_dung_tham_xet = noi_dung_tham_xet
        yeu_cau_chung_chi.noi_dung_yeu_cau_bo_sung = noi_dung_yeu_cau_bo_sung
        db.session.commit()

        return {"msg": "Đổi trạng thái hồ sơ thành công "}, HttpCode.OK

# Update man hinh du thao trinh cap , yeu cau bo sung, tu choi


class YeuCauChungChiUpdateThongTin(Resource):
    @jwt_required()
    def put(self, id):
        user = User.query.filter(User.id == current_user.id).first()
        user.assigned_role
        yeu_cau_cchnd: YeuCauChungChiHanhNghe = YeuCauChungChiHanhNghe.query.filter(
            YeuCauChungChiHanhNghe.id == id).first()
        trang_thai_ho_so = request.json.get("trang_thai_ho_so")

        if trang_thai_ho_so == '3' or trang_thai_ho_so == '7':

            ly_do_tu_choi = request.json.get("ly_do_tu_choi")
            if ly_do_tu_choi is None or ly_do_tu_choi == '':
                return {"msg": "Vui lòng nhập lý do từ chối"}, HttpCode.BadRequest

            if "chuyenvien" in [x.ten_en for x in user.assigned_role]:
                yeu_cau_cchnd.ly_do_tu_choi_chuyen_vien = ly_do_tu_choi
            if "lanhdao" in [x.ten_en for x in user.assigned_role]:
                yeu_cau_cchnd.ly_do_tu_choi_lanh_dao = ly_do_tu_choi

            # PUSH NOTIFICATION
            fcm_tokens = redisdb.mget(redisdb.keys(pattern="fcm_token:"+str(yeu_cau_cchnd.nhan_vien_id)+":*"))
            tieu_de = f"Từ chối hồ sơ"
            noi_dung = f"{current_user.ho_ten} đã từ chối yêu cầu cấp chứng chỉ hành nghề dược của bạn vào lúc {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
            thong_bao = ThongBao(tieu_de=tieu_de, noi_dung=noi_dung, nhan_vien_id=yeu_cau_cchnd.nhan_vien_id, dinh_kem={
                                 "yeu_cau_cchnd_id": str(yeu_cau_cchnd.id)})
            if fcm_tokens and len(fcm_tokens) > 0:
                send_push_notification(tieu_de, noi_dung,
                                       registration_tokens=fcm_tokens, to_all=False)
            db.session.add(thong_bao)

            yeu_cau_cchnd.trang_thai_ho_so = trang_thai_ho_so
            db.session.commit()
            return {"msg": "Từ Chối Hồ Sơ Thành Công"}, HttpCode.OK
        if trang_thai_ho_so == '5' or trang_thai_ho_so == '8':

            # noi_dung_tham_xet = request.json.get("noi_dung_tham_xet")
            noi_dung_yeu_cau_bo_sung = request.json.get("noi_dung_yeu_cau_bo_sung")
            # if noi_dung_tham_xet is None:
            #     return {"msg": "Vui lòng nhập nội dung thẩm xét"}, HttpCode.BadRequest
            if noi_dung_yeu_cau_bo_sung is None:
                return {"msg": "Vui lòng nhập yêu cầu bổ sung"}, HttpCode.BadRequest

            if "chuyenvien" in [x.ten_en for x in user.assigned_role]:
                yeu_cau_cchnd.noi_dung_yeu_cau_bo_sung_chuyen_vien = noi_dung_yeu_cau_bo_sung
            if "lanhdao" in [x.ten_en for x in user.assigned_role]:
                yeu_cau_cchnd.noi_dung_yeu_cau_bo_sung_lanh_dao = noi_dung_yeu_cau_bo_sung

            # PUSH NOTIFICATION
            fcm_tokens = redisdb.mget(redisdb.keys(pattern="fcm_token:"+str(yeu_cau_cchnd.nhan_vien_id)+":*"))
            tieu_de = f"Yêu cầu bổ sung hồ sơ"
            noi_dung = f"{current_user.ho_ten} yêu cầu bổ sung vào hồ sơ yêu cầu cấp chứng chỉ hành nghề dược của bạn vào lúc {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
            thong_bao = ThongBao(tieu_de=tieu_de, noi_dung=noi_dung, nhan_vien_id=yeu_cau_cchnd.nhan_vien_id, dinh_kem={
                                 "yeu_cau_cchnd_id": str(yeu_cau_cchnd.id)})
            if fcm_tokens and len(fcm_tokens) > 0:
                send_push_notification(tieu_de, noi_dung,
                                       registration_tokens=fcm_tokens, to_all=False)
            db.session.add(thong_bao)

            yeu_cau_cchnd.trang_thai_ho_so = trang_thai_ho_so
            db.session.commit()
            return {"msg": "Chuyển Hồ Sơ về Yêu Cầu Bổ Sung Thành Công"}, HttpCode.OK
        elif trang_thai_ho_so == '12':
            if "chuyenvien" in [x.ten_en for x in user.assigned_role]:
                yeu_cau_cchnd.trang_thai_ho_so = trang_thai_ho_so
                if request.json.get("noi_dung_yeu_cau_bo_sung") is not None:
                    yeu_cau_cchnd.noi_dung_yeu_cau_bo_sung_chuyen_vien = request.json. get("noi_dung_yeu_cau_bo_sung")
                db.session.commit()
                return {"msg": "Gửi yêu cầu bổ sung chờ phê duyệt thành công"}, HttpCode.OK

        return {"msg": "Người Dùng không có vai trò thụ lý hồ sơ"}, HttpCode.UnAuthorized


class PutCCHNDDuThao(Resource):
    @jwt_required()
    def put(self, id):

        yeucau_cchnd = YeuCauChungChiHanhNghe.query.filter(YeuCauChungChiHanhNghe.id == id).first()
        user = User.query.filter(User.id == current_user.id).first()
        user.assigned_role
        schema = YeuCauChungChiHanhNgheSchema(partial=True)

        req = {
            "ho": request.json.get("ho"),
            "ten": request.json.get("ten"),
            "ngay_sinh": request.json.get("ngay_sinh"),
            "gioi_tinh": request.json.get("gioi_tinh"),
            "quan_huyen_id": request.json.get("quan_huyen_thuong_tru_id"),
            "tinh_thanh_id": request.json.get("tinh_thanh_thuong_tru_id"),
            "xa_phuong_id": request.json.get("xa_phuong_thuong_tru_id"),
            "quan_huyen_hien_nay_id": request.json.get("quan_huyen_hien_nay_id"),
            "tinh_thanh_hien_nay_id": request.json.get("tinh_thanh_hien_nay_id"),
            "xa_phuong_hien_nay_id": request.json.get("xa_phuong_hien_nay_id"),
            "ma_cong_dan": request.json.get("ma_cong_dan"),
            "ngay_cap": request.json.get("ngay_cap"),
            "noi_cap": request.json.get("noi_cap"),
            "dien_thoai": request.json.get("dien_thoai"),
            "email": request.json.get("email"),
            "so_nha": request.json.get("so_nha"),
            "so_nha_thuong_tru": request.json.get("so_nha_thuong_tru")
        }
        doi_tuong = yeucau_cchnd.doi_tuong
        doi_tuong["ho"] = req["ho"]
        doi_tuong["ten"] = req["ten"]
        doi_tuong["ngay_sinh"] = req["ngay_sinh"]
        doi_tuong["gioi_tinh"] = req["gioi_tinh"]
        doi_tuong["quan_huyen_id"] = req["quan_huyen_id"]
        doi_tuong["tinh_thanh_id"] = req["tinh_thanh_id"]
        doi_tuong["xa_phuong_id"] = req["xa_phuong_id"]
        doi_tuong["quan_huyen_hien_nay_id"] = req["quan_huyen_hien_nay_id"]
        doi_tuong["tinh_thanh_hien_nay_id"] = req["tinh_thanh_hien_nay_id"]
        doi_tuong["xa_phuong_hien_nay_id"] = req["xa_phuong_hien_nay_id"]
        doi_tuong["ma_cong_dan"] = req["ma_cong_dan"]
        doi_tuong["ngay_cap"] = req["ngay_cap"]
        doi_tuong["noi_cap"] = req["noi_cap"]
        doi_tuong["dien_thoai"] = req["dien_thoai"]
        doi_tuong["email"] = req["email"]
        doi_tuong["so_nha"] = req["so_nha"]
        doi_tuong["so_nha_thuong_tru"] = req["so_nha_thuong_tru"]

        xa_phuong = XaPhuong.query.filter(XaPhuong.id == req["xa_phuong_hien_nay_id"]).first()
        quan_huyen = QuanHuyen.query.filter(QuanHuyen.id == req["quan_huyen_hien_nay_id"]).first()
        tinh_thanh = TinhThanh.query.filter(TinhThanh.id == req["tinh_thanh_hien_nay_id"]).first()

        xa_phuong_thuong_tru = XaPhuong.query.filter(XaPhuong.id == req["xa_phuong_id"]).first()
        quan_huyen_thuong_tru = QuanHuyen.query.filter(QuanHuyen.id == req["quan_huyen_id"]).first()
        tinh_thanh_thuong_tru = TinhThanh.query.filter(TinhThanh.id == req["tinh_thanh_id"]).first()

        doi_tuong["dia_chi"] = req["so_nha"] + ", " + xa_phuong.ten + ", " + quan_huyen.ten + ", " + tinh_thanh.ten
        doi_tuong["dia_chi_thuong_tru"] = req["so_nha_thuong_tru"] + ", " + xa_phuong_thuong_tru.ten + \
            ", " + quan_huyen_thuong_tru.ten + ", " + tinh_thanh_thuong_tru.ten

        vi_tri_hanh_nghe_ids = request.json.get("vi_tri_hanh_nghe_ids")

        vi_tri_hanh_nghe_list = ViTriHanhNghe.query.filter(ViTriHanhNghe.id.in_(vi_tri_hanh_nghe_ids)).all()
        arr = {"id": []}
        for vi_tri_hanh_nghe in vi_tri_hanh_nghe_list:
            arr["id"].append(str(vi_tri_hanh_nghe.id))

        yeucau_cchnd.vi_tri_hanh_nghe_cchn = arr

        pham_vi_hoat_dong_ids = request.json.get("pham_vi_hoat_dong_chuyen_mon_ids")

        pham_vi_hoat_dong_chuyen_mon_list = PhamViHoatDongChuyenMon.query.filter(
            PhamViHoatDongChuyenMon.id.in_(pham_vi_hoat_dong_ids)).all()
        arr_2 = {"id": []}
        for pham_vi_hoat_dong in pham_vi_hoat_dong_chuyen_mon_list:
            arr_2["id"].append(str(pham_vi_hoat_dong.id))

        yeucau_cchnd.pham_vi_chuyen_mon = arr_2

        yeu_cau_phien_dich = request.json.get("yeu_cau_phien_dich")

        if yeu_cau_phien_dich == True:
            yeucau_cchnd.yeu_cau_phien_dich = True
        elif yeu_cau_phien_dich == False:
            yeucau_cchnd.yeu_cau_phien_dich = False

        req_2 = {
            "noi_dung_tham_xet": request.json.get("noi_dung_tham_xet"),
            "noi_dung_de_nghi": request.json.get("noi_dung_de_nghi"),
        }

        yeucau_cchnd: YeuCauChungChiHanhNghe = schema.load(req_2, instance=yeucau_cchnd)

        if "lanhdao" in [x.ten_en for x in user.assigned_role]:
            yeucau_cchnd.y_kien_lanh_dao = request.json.get("y_kien_lanh_dao")

        trang_thai_ho_so = request.json.get("trang_thai_ho_so")

        yeucau_cchnd.trang_thai_ho_so = trang_thai_ho_so

        if trang_thai_ho_so == '5':
            # PUSH NOTIFICATION
            fcm_tokens = redisdb.mget(redisdb.keys(pattern="fcm_token:"+str(yeucau_cchnd.nhan_vien_id)+":*"))
            tieu_de = f"Yêu cầu bổ sung hồ sơ"
            noi_dung = f"{current_user.ho_ten} yêu cầu bổ sung vào hồ sơ yêu cầu cấp chứng chỉ hành nghề dược của bạn vào lúc {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
            thong_bao = ThongBao(tieu_de=tieu_de, noi_dung=noi_dung, nhan_vien_id=yeucau_cchnd.nhan_vien_id, dinh_kem={
                                 "yeu_cau_cchnd_id": str(yeucau_cchnd.id)})
            if fcm_tokens and len(fcm_tokens) > 0:
                send_push_notification(tieu_de, noi_dung,
                                       registration_tokens=fcm_tokens, to_all=False)
            db.session.add(thong_bao)
            db.session.commit()

            return {"msg": "Chuyển Hồ Sơ về Yêu Cầu Bổ Sung Thành Công"}, HttpCode.OK
        if trang_thai_ho_so == '6':
            db.session.commit()
            return {"msg": "Chuyển Hồ Sơ Lên Lãnh Đạo Thành Công"}, HttpCode.OK
        if trang_thai_ho_so == '7':
            db.session.commit()
            return {"msg": "Hồ Sơ Bị Từ Chối Thành Công"}, HttpCode.OK
        if trang_thai_ho_so == '8':
            # PUSH NOTIFICATION
            fcm_tokens = redisdb.mget(redisdb.keys(pattern="fcm_token:"+str(yeucau_cchnd.nhan_vien_id)+":*"))
            tieu_de = f"Yêu cầu bổ sung hồ sơ"
            noi_dung = f"{current_user.ho_ten} yêu cầu bổ sung vào hồ sơ yêu cầu cấp chứng chỉ hành nghề dược của bạn vào lúc {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
            thong_bao = ThongBao(tieu_de=tieu_de, noi_dung=noi_dung, nhan_vien_id=yeucau_cchnd.nhan_vien_id, dinh_kem={
                                 "yeu_cau_cchnd_id": str(yeucau_cchnd.id)})
            if fcm_tokens and len(fcm_tokens) > 0:
                send_push_notification(tieu_de, noi_dung,
                                       registration_tokens=fcm_tokens, to_all=False)
            db.session.add(thong_bao)
            db.session.commit()
            return {"msg": "Chuyển Hồ Sơ Yêu Cầu Bổ Sung Thành Công"}, HttpCode.OK
        if trang_thai_ho_so == '9':
            loai_ma_cchnd = LOAIMACHUNGCHI.query.filter(LOAIMACHUNGCHI.mac_dinh == True).first()
            loai_ma_cchnd.so_da_cap = loai_ma_cchnd.so_da_cap + 1
            yeucau_cchnd.loai_ma_cchnd = loai_ma_cchnd.id
            yeucau_cchnd.so_cchnd = loai_ma_cchnd.so_da_cap
            yeucau_cchnd.lanh_dao_duyet_id = current_user.id
            db.session.commit()
            return {"msg": "Trình Hồ Sơ Lên HĐTV Thành Công"}, HttpCode.OK
        if trang_thai_ho_so == '4':
            db.session.commit()
            return {"msg": "Lưu Hồ Sơ Thành Công"}, HttpCode.OK

        return {"msg": "Internal Server Error "}, HttpCode.InternalError

# doi nhieu trang thai ho so


class ChangeMultiStatus(Resource):
    @jwt_required()
    def put(self):

        ids = request.json.get("ids")
        trang_thai_ho_so = request.json.get("trang_thai_ho_so")
        noi_dung_yeu_cau_bo_sung = request.json.get("noi_dung_yeu_cau_bo_sung")
        ly_do_tu_choi = request.json.get("ly_do_tu_choi")
        so_quyet_dinh = request.json.get("so_quyet_dinh")
        ngay_quyet_dinh = request.json.get("ngay_quyet_dinh")
        user = current_user
        user.assigned_role
        if ids is None:
            return {"msg": "Chưa có hồ sơ nào được chọn"}, HttpCode.BadRequest

        yeucau_cchnd_list = YeuCauChungChiHanhNghe.query.filter(YeuCauChungChiHanhNghe.id.in_(ids)).all()

        for yeu_cau_cchnd in yeucau_cchnd_list:

            yeu_cau_cchnd.trang_thai_ho_so = trang_thai_ho_so

            if trang_thai_ho_so == '9':
                loai_ma_cchnd = LOAIMACHUNGCHI.query.filter(LOAIMACHUNGCHI.mac_dinh == True).first()
                loai_ma_cchnd.so_da_cap = loai_ma_cchnd.so_da_cap + 1
                yeu_cau_cchnd.loai_ma_cchnd = loai_ma_cchnd.id
                yeu_cau_cchnd.so_cchnd = loai_ma_cchnd.so_da_cap
                yeu_cau_cchnd.lanh_dao_duyet_id = current_user.id

                db.session.commit()

            elif trang_thai_ho_so == '8':
                if noi_dung_yeu_cau_bo_sung is None:
                    return {"msg": "Vui Lòng Nhập Lý Do Yêu Cầu Bổ Sung"}, HttpCode.BadRequest
                yeu_cau_cchnd.noi_dung_yeu_cau_bo_sung_lanh_dao = noi_dung_yeu_cau_bo_sung

                # PUSH NOTIFICATION
                fcm_tokens = redisdb.mget(redisdb.keys(pattern="fcm_token:"+str(yeu_cau_cchnd.nhan_vien_id)+":*"))
                tieu_de = f"Yêu cầu bổ sung hồ sơ"
                noi_dung = f"{current_user.ho_ten} yêu cầu bổ sung vào hồ sơ yêu cầu cấp chứng chỉ hành nghề dược của bạn vào lúc {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
                thong_bao = ThongBao(tieu_de=tieu_de, noi_dung=noi_dung, nhan_vien_id=yeu_cau_cchnd.nhan_vien_id, dinh_kem={
                    "yeu_cau_cchnd_id": str(yeu_cau_cchnd.id)})
                if fcm_tokens and len(fcm_tokens) > 0:
                    send_push_notification(tieu_de, noi_dung,
                                           registration_tokens=fcm_tokens, to_all=False)
                db.session.add(thong_bao)
                db.session.commit()

            elif trang_thai_ho_so == '7':
                if ly_do_tu_choi is None:
                    return {"msg": "Vui Lòng Nhập Lý Do Từ Chối"}, HttpCode.BadRequest
                yeu_cau_cchnd.ly_do_tu_choi_lanh_dao = ly_do_tu_choi
                db.session.commit()

            elif trang_thai_ho_so == '2':
                db.session.commit()

            elif trang_thai_ho_so == '10':
                if "chuyenvienhoidong" in [x.ten_en for x in user.assigned_role]:
                    db.session.commit()
                    return {"msg": "Chuyển Văn Thư Thành Công"}, HttpCode.OK
                if "vanthu" in [x.ten_en for x in user.assigned_role]:
                    if so_quyet_dinh is None:
                        return {"msg": "Vui Lòng nhập số quyết định"}, HttpCode.InternalError
                    yeu_cau_cchnd.so_quyet_dinh = so_quyet_dinh
                    yeu_cau_cchnd.ngay_quyet_dinh = ngay_quyet_dinh
                    db.session.commit()
            elif trang_thai_ho_so == '5':
                # PUSH NOTIFICATION
                fcm_tokens = redisdb.mget(redisdb.keys(pattern="fcm_token:"+str(yeu_cau_cchnd.nhan_vien_id)+":*"))
                tieu_de = f"Yêu cầu bổ sung hồ sơ"
                noi_dung = f"{current_user.ho_ten} yêu cầu bổ sung vào hồ sơ yêu cầu cấp chứng chỉ hành nghề dược của bạn vào lúc {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
                thong_bao = ThongBao(tieu_de=tieu_de, noi_dung=noi_dung, nhan_vien_id=yeu_cau_cchnd.nhan_vien_id, dinh_kem={
                    "yeu_cau_cchnd_id": str(yeu_cau_cchnd.id)})
                if fcm_tokens and len(fcm_tokens) > 0:
                    send_push_notification(tieu_de, noi_dung,
                                           registration_tokens=fcm_tokens, to_all=False)
                db.session.add(thong_bao)
                db.session.commit()
            elif trang_thai_ho_so == '4':
                db.session.commit()
            elif trang_thai_ho_so == '11':
                if so_quyet_dinh is None:
                    return {"msg": "Vui Lòng nhập số quyết định"}, HttpCode.InternalError

                doi_tuong = yeu_cau_cchnd.doi_tuong
                user = User.query.filter(User.id == yeu_cau_cchnd.nhan_vien_id).first()
                user_schema = NhanVienSchema(partial=True)
                chung_chi_hanh_nghe = ChungChiHanhNghe.query.filter(
                    ChungChiHanhNghe.id == yeu_cau_cchnd.nhan_vien_id).first()
                chungchi_schema = ChungChiHanhNgheSchema(partial=True)
                ma_cchnd = LOAIMACHUNGCHI.query.filter(LOAIMACHUNGCHI.id == yeu_cau_cchnd.loai_ma_cchnd).first()
                req = {
                    "ho": doi_tuong["ho"],
                    "ten": doi_tuong["ten"],
                    "ngay_sinh": doi_tuong["ngay_sinh"],
                    "gioi_tinh": doi_tuong["gioi_tinh"],
                    "quan_huyen_id": doi_tuong["quan_huyen_id"],
                    "tinh_thanh_id": doi_tuong["tinh_thanh_id"],
                    "xa_phuong_id": doi_tuong["xa_phuong_id"],
                    "dia_chi_thuong_tru": doi_tuong["dia_chi_thuong_tru"],
                    "quan_huyen_hien_nay_id": doi_tuong["quan_huyen_hien_nay_id"],
                    "tinh_thanh_hien_nay_id": doi_tuong["tinh_thanh_hien_nay_id"],
                    "xa_phuong_hien_nay_id": doi_tuong["xa_phuong_hien_nay_id"],
                    "dia_chi": doi_tuong["dia_chi"],
                    "ma_cong_dan": doi_tuong["ma_cong_dan"],
                    "ngay_cap": doi_tuong["ngay_cap"],
                    "noi_cap": doi_tuong["noi_cap"],
                    "dien_thoai": doi_tuong["dien_thoai"],
                    "email": doi_tuong["email"],
                    "da_cap_chung_chi": True
                }
                req_2 = {
                    "so_giay_phep": yeu_cau_cchnd.so_cchnd + "/" + ma_cchnd.ma_chung_chi,
                    "ngay_hieu_luc": yeu_cau_cchnd.ngay_hieu_luc,
                    "lan_cap_thu": yeu_cau_cchnd.lan_cap_thu,
                    "hinh_thuc_thi": yeu_cau_cchnd.hinh_thuc,
                    "so_quyet_dinh": yeu_cau_cchnd.so_quyet_dinh,
                    "ngay_quyet_dinh": yeu_cau_cchnd.ngay_quyet_dinh,
                }
                user = user_schema.load(req, instance=user)
                if chung_chi_hanh_nghe:
                    chung_chi_hanh_nghe = chungchi_schema.load(req_2, instance=chung_chi_hanh_nghe)
                elif not chung_chi_hanh_nghe:
                    check_exist = ChungChiHanhNghe.query.filter(ChungChiHanhNghe.nhan_vien_id == user.id).first()
                    if not check_exist:
                        chungchi_schema_new = ChungChiHanhNgheSchema()
                        chung_chi_hanh_nghe = chungchi_schema_new.load(req_2)
                        chung_chi_hanh_nghe.nhan_vien_id = user.id
                        db.session.add(chung_chi_hanh_nghe)
                yeu_cau_cchnd.so_quyet_dinh = so_quyet_dinh
                yeu_cau_cchnd.ngay_quyet_dinh = ngay_quyet_dinh

                # PUSH NOTIFICATION
                fcm_tokens = redisdb.mget(redisdb.keys(pattern="fcm_token:"+str(yeu_cau_cchnd.nhan_vien_id)+":*"))
                tieu_de = f"Hoàn thành"
                noi_dung = f"{current_user.ho_ten} đã phê duyệt hồ sơ của bạn vào lúc {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
                thong_bao = ThongBao(tieu_de=tieu_de, noi_dung=noi_dung, nhan_vien_id=yeu_cau_cchnd.nhan_vien_id, dinh_kem={
                                     "yeu_cau_cchnd_id": str(yeu_cau_cchnd.id)})
                if fcm_tokens and len(fcm_tokens) > 0:
                    send_push_notification(tieu_de, noi_dung,
                                           registration_tokens=fcm_tokens, to_all=False)
                db.session.add(thong_bao)

                db.session.commit()

        if trang_thai_ho_so == '9':
            return {"msg": "Trình Hồ Sơ Lên HĐTV Thành Công"}, HttpCode.OK

        if trang_thai_ho_so == '8':

            return {"msg": "Chuyển Hồ Sơ Yêu Cầu Bổ Sung Thành Công"}, HttpCode.OK

        if trang_thai_ho_so == '7':
            return {"msg": "Hồ Sơ Bị Từ Chối Thành Công"}, HttpCode.OK

        if trang_thai_ho_so == '2':
            return {"msg": "Chuyển chuyên viên thụ lý thành công"}, HttpCode.OK

        if trang_thai_ho_so == '10':
            return {"msg": "Lưu Hồ Sơ thành công"}, HttpCode.OK

        if trang_thai_ho_so == '11':
            return {"msg": "Hoàn thành hồ sơ thành công"}, HttpCode.OK

        if trang_thai_ho_so == '5':

            return {"msg": "Yêu cầu bổ sung thành công"}, HttpCode.OK

        if trang_thai_ho_so == '4':
            return {"msg": "Chuyển thụ lý hồ sơ thành công"}, HttpCode.OK

        return {"msg": "Internal Server Error "}, HttpCode.InternalError

# chuyen vien hoi dong update ho so


class UpdateCCHNDChuyenVienHoiDong(Resource):
    @jwt_required()
    def put(self, id):
        req = {
            "loai_ma_cchnd": request.json.get("loai_ma_cchnd"),
            "so_cchnd": request.json.get("so_cchnd"),
            "lan_cap_thu": request.json.get("lan_thu"),
            "hinh_thuc": request.json.get("hinh_thuc"),
            "hoi_dong_id": request.json.get("hoi_dong_id"),
            "ngay_hieu_luc": request.json.get("ngay_hieu_luc"),
            "ngay_het_han": request.json.get("ngay_het_han"),
            "thay_the_cchnd": request.json.get("thay_the_cchnd"),
            "ngay_cap_cchnd_cu": request.json.get("ngay_het_han_cchnd_cu"),
            "noi_dung_tham_xet": request.json.get("noi_dung_tham_xet"),
            "noi_dung_de_nghi": request.json.get("noi_dung_de_nghi"),
            "yeu_cau_phien_dich": request.json.get("yeu_cau_phien_dich")
        }
        trang_thai_ho_so = request.json.get("trang_thai_ho_so")

        schema = YeuCauChungChiHanhNgheSchema(partial=True)

        yeucau_cchnd = YeuCauChungChiHanhNghe.query.filter(YeuCauChungChiHanhNghe.id == id).first()

        if trang_thai_ho_so == "9":
            yeucau_cchnd = schema.load(req, instance=yeucau_cchnd)
            yeucau_cchnd.trang_thai_ho_so = trang_thai_ho_so
            db.session.commit()
            return {"msg": "Lưu Hồ Sơ Thành Công"}, HttpCode.OK

        if trang_thai_ho_so == "10":
            yeucau_cchnd = schema.load(req, instance=yeucau_cchnd)
            yeucau_cchnd.trang_thai_ho_so = trang_thai_ho_so
            db.session.commit()

            return {"msg": "Chuyển Văn Thư Thành Công"}, HttpCode.OK

        if trang_thai_ho_so == "2":
            yeucau_cchnd.so_cchnd = None
            yeucau_cchnd.trang_thai_ho_so = trang_thai_ho_so
            db.session.commit()
            return {"msg": "Chuyển chuyên viên thụ lý thành công"}, HttpCode.OK

            if request.form.get("delete_dinh_kem_van_bang_chuyen_mon[]") and chung_chi.dinh_kem_van_bang_chuyen_mon:
                chung_chi.dinh_kem_van_bang_chuyen_mon = [
                    x for x in chung_chi.dinh_kem_van_bang_chuyen_mon if x["url"] not in request.form.getlist("delete_dinh_kem_van_bang_chuyen_mon[]")]


def upload_images(images, target_list, error_list=[]):
    if images and len(images) > 0:
        links, errors = UploadMinio.upload_duocsi(images, many=True)
        if target_list:
            target_list.extend(links)
        else:
            target_list[:] = links
        if errors:
            error_list.extend(errors)
        return target_list


def remove_images(target_urls, target_list):
    if target_urls and len(target_urls) > 0 and target_list:
        target_list[:] = [image for image in target_list if image["url"]
                          not in target_urls]
