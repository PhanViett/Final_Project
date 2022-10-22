
from datetime import datetime
from functools import partial
import json
from re import L
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError
from application.models.bang_cap import BangCap
from application.models.danhmuc_noi_tot_nghiep import NoiTotNghiep
from application.models.danhmuc_van_bang_chuyen_mon import VanBangChuyenMon
from application.schemas.danhmuc_noi_tot_nghiep import NoiTotNghiepSchema
from application.schemas.danhmuc_van_bang_chuyen_mon import VanBangChuyenMonSchema
from application.schemas.dao_tao import DaotaoSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
from application.schemas.bang_cap import BangCapDuocSiSchema, BangCapSchema
from application.extensions import db
from application.commons.pagination import paginate
from sqlalchemy.orm import joinedload, noload, defaultload, load_only


class BangCapResource(Resource):
    @jwt_required()
    def post(self):
        schema = BangCapSchema()
        req = {
            "so_hieu": request.form.get('so_hieu', None) or None,
            "loai_hinh_dao_tao": request.form.get('loai_hinh_dao_tao', None) or None,
            "noi_tot_nghiep_id": request.form.get('noi_tot_nghiep_id', None) or None,
            "van_bang_chuyen_mon_id": request.form.get('van_bang_chuyen_mon_id', None) or None,
            "nganh_dao_tao": request.form.get('nganh_dao_tao', None) or None,
            "xep_hang": request.form.get('xep_hang', None) or None,
            "danh_hieu": request.form.get('danh_hieu', None) or None,
            "ghi_chu": request.form.get('ghi_chu', None) or None,
            "hinh_thuc_dao_tao": request.form.get('hinh_thuc_dao_tao', None) or None,
        }
        try:
            bang_cap: BangCap = schema.load(req)
            ngay_cap = request.form.get("ngay_cap")
            bang_cap.ngay_cap = ngay_cap
            if current_user.assigned_role[0].ten_en != "duocsi":
                bang_cap.nhan_vien_id = request.form.get('nhan_vien_id')
            else:
                bang_cap.nhan_vien_id = current_user.id
            db.session.add(bang_cap)
            db.session.flush()
        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest

        upload_errors = []
        chung_tu_dinh_kem = request.files.getlist('chung_tu_dinh_kem[]')
        if chung_tu_dinh_kem and len(chung_tu_dinh_kem) > 0:
            danh_sach_chung_tu_dk, errors = UploadMinio.upload_duocsi(chung_tu_dinh_kem, many=True)
            bang_cap.chung_tu_dinh_kem.extend(danh_sach_chung_tu_dk)
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_anh_chan_dung[]"):
            bang_cap.chung_tu_dinh_kem = [x for x in bang_cap.chung_tu_dinh_kem if x["url"]
                                          not in request.form.getlist("delete_dinh_kem_anh_chan_dung[]")]

        db.session.commit()
        return {"msg": "Tạo thành công", "results": schema.dump(bang_cap), "upload_errors": upload_errors}, HttpCode.Created

    @jwt_required()
    def get(self):
        schema = BangCapSchema(many=True)
        nhan_vien_id = request.args.get('nhan_vien_id')
        bang_cap = BangCap.query.filter(BangCap.nhan_vien_id == nhan_vien_id)
        if bang_cap is None:
            return {"errors": "No data"},  HttpCode.InternalError
        return paginate(bang_cap, schema)


class BangCapById(Resource):
    @jwt_required()
    def put(self, id):
        schema = BangCapSchema(partial=True)
        bang_cap = BangCap.query.filter(BangCap.id == id).first()
        if bang_cap is None:
            return {"errors": "No data"},  HttpCode.InternalError
        req = {
            "so_hieu": request.form.get('so_hieu', None) or None,
            "loai_hinh_dao_tao": request.form.get('loai_hinh_dao_tao', None) or None,
            "noi_tot_nghiep_id": request.form.get('noi_tot_nghiep_id', None) or None,
            "van_bang_chuyen_mon_id": request.form.get('van_bang_chuyen_mon_id', None) or None,
            "nganh_dao_tao": request.form.get('nganh_dao_tao', None) or None,
            "xep_hang": request.form.get('xep_hang', None) or None,
            "danh_hieu": request.form.get('danh_hieu', None) or None,
            "ghi_chu": request.form.get('ghi_chu', None) or None,
            "hinh_thuc_dao_tao": request.form.get('hinh_thuc_dao_tao', None) or None,
        }

        try:
            bang_cap: BangCap = schema.load(req, instance=bang_cap)
            ngay_cap = request.form.get("ngay_cap")
            bang_cap.ngay_cap = ngay_cap
            bang_cap.nhan_vien_id = current_user.id
            db.session.flush()
            # db.session.add(bang_cap)
            # db.session.flush()
        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest

        upload_errors = []
        chung_tu_dinh_kem = request.files.getlist('chung_tu_dinh_kem[]')
        if chung_tu_dinh_kem and len(chung_tu_dinh_kem) > 0:
            danh_sach_chung_tu_dk, errors = UploadMinio.upload_duocsi(chung_tu_dinh_kem, many=True)
            bang_cap.chung_tu_dinh_kem.extend(danh_sach_chung_tu_dk)
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_anh_chan_dung[]"):
            bang_cap.chung_tu_dinh_kem = [x for x in bang_cap.chung_tu_dinh_kem if x["url"]
                                          not in request.form.getlist("delete_dinh_kem_anh_chan_dung[]")]

        db.session.commit()
        return {"msg": "Cập nhật thành công", "results": schema.dump(bang_cap), "upload_errors": upload_errors}, HttpCode.OK

    @jwt_required()
    def get(self, id):
        schema = BangCapSchema()
        vanbangSchema = VanBangChuyenMonSchema()
        noitotnhiepSchema = NoiTotNghiepSchema()
        bang_cap = BangCap.query.filter(BangCap.id == id).first()
        van_bang_chuyen_mon = VanBangChuyenMon.query.filter(
            VanBangChuyenMon.id == bang_cap.van_bang_chuyen_mon_id).first()
        noi_tot_nghiep = NoiTotNghiep.query.filter(NoiTotNghiep.id == bang_cap.noi_tot_nghiep_id).first()
        if bang_cap is None:
            return {"errors": "No data"},  HttpCode.InternalError
        return {
            "results": {
                "bang_cap": schema.dump(bang_cap),
                "van_bang": vanbangSchema.dump(van_bang_chuyen_mon),
                "tot_nghiep": noitotnhiepSchema.dump(noi_tot_nghiep)
            }
        }, HttpCode.OK

    @jwt_required()
    def delete(self, id):
        schema = BangCapSchema()
        bang_cap = BangCap.query.filter(BangCap.id == id).first()
        if bang_cap is None:
            return {"errors": "No data"},  HttpCode.InternalError
        db.session.delete(bang_cap)
        db.session.commit()

        return {"msg": "Xóa thành công"}, HttpCode.OK


class BangCapGetList(Resource):
    # @jwt_required()
    # def post(self):
    #     schema = BangCapSchema(many =True)
    #     query = BangCap.query
    #     if not request.json:
    #         query = query.order_by(BangCap.updated_at.desc())
    #         return paginate(query, schema), HttpCode.OK

    #     if "trang_thai" in request.json:
    #         if request.json.get("trang_thai") != None:
    #             query = query.filter(
    #                 BangCap.trang_thai == request.json.get("trang_thai")
    #             )
    #     return paginate(query,schema), HttpCode.OK
    # @jwt_required()
    # def post(self):
    #     schema = BangCapSchema(many =True)
    #     nhan_vien_id = request.json.get("nhan_vien_id")
    #     query = BangCap.query
    #     if not request.json:
    #         query = query.order_by(BangCap.updated_at.desc())
    #         return paginate(query, schema), HttpCode.OK

    #     if "nhan_vien_id" in request.json:
    #         query = query.filter(BangCap.nhan_vien_id == nhan_vien_id)
    #         return paginate(query,schema), HttpCode.OK

    #     if len(query.all()) <= 0:
    #          return {"msg":"không có bằng cấp!"}
    #     return paginate(query,schema), HttpCode.OK
    @jwt_required()
    def post(get):
        schema = BangCapDuocSiSchema(many=True)
        id = request.json.get("nhan_vien_id")
        query = BangCap.query.filter(BangCap.nhan_vien_id == id)
        # if not data:
        #     query = query.order_by(BangCap.updated_at.desc())

        # if data.get("search_ten", None):
        #     search_ten = data["search_ten"]
        #     query = query.filter(BangCap.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))

        # if "nhan_vien_id" in request.json:
        #     query = query.filter(BangCap.nhan_vien_id == nhan_vien_id)

        query = query.order_by(BangCap.updated_at.desc())
        res = paginate(query, schema)
        return res, HttpCode.OK
