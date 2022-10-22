
from functools import partial
import json
from re import L
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError
from application.models.co_so_thuc_hanh import CoSoThucHanh
from application.models.noi_dung_thuc_hanh import NoiDungThucHanh
from application.models.quan_huyen import QuanHuyen
from application.models.tinh_thanh import TinhThanh
from application.models.xa_phuong import XaPhuong
from application.schemas.co_so_thuc_hanh import CoSoThucHanhDisPlaySchema, CoSoThucHanhSchema
from application.schemas.tinh_thanh import TinhThanhSchema
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
from application.extensions import db
from application.commons.pagination import paginate
class CoSoThucHanhResource(Resource):
    @jwt_required()
    def post(self):
        schema = CoSoThucHanhSchema()
        req = {
            "ma_co_so": request.form.get('ma_co_so',None) or None,
            "ten_co_so": request.form.get('ten_co_so',None) or None,
            "dia_chi_co_so": request.form.get('dia_chi_co_so',None) or None,
            "tu_ngay":request.form.get('tu_ngay',None) or None,
            "den_ngay":request.form.get('den_ngay',None) or None,
            "ten_nguoi_phu_trach": request.form.get('ten_nguoi_phu_trach',None) or None,
            "dien_thoai_nguoi_phu_trach": request.form.get('dien_thoai_nguoi_phu_trach',None) or None,
            "noi_dung_khac": request.form.get('noi_dung_khac',None) or None,
            "so_nha": request.form.get('so_nha',None) or None,
            "quan_huyen_id": request.form.get('quan_huyen_id',None) or None,
            "tinh_thanh_id": request.form.get('tinh_thanh_id',None) or None,
            "xa_phuong_id": request.form.get('xa_phuong_id',None) or None,
        }
        try:
            co_so:CoSoThucHanh = schema.load(req)
            if current_user.assigned_role[0].ten_en != "duocsi":
                co_so.nhan_vien_id = request.form.get('nhan_vien_id')
            else: 
                co_so.nhan_vien_id = current_user.id
            db.session.add(co_so)
            db.session.flush()
        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest
        
        chung_tu_dinh_kem = request.files.getlist('chung_tu_dinh_kem[]') if "chung_tu_dinh_kem[]" in request.files else None
        upload_errors = []
        chung_tu_dinh_kem = request.files.getlist('chung_tu_dinh_kem[]')
        if chung_tu_dinh_kem and len(chung_tu_dinh_kem) > 0:
            danh_sach_chung_tu_dk,errors = UploadMinio.upload_duocsi(chung_tu_dinh_kem, many=True)
            co_so.chung_tu_dinh_kem.extend(danh_sach_chung_tu_dk)
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_anh_chan_dung[]"):
            co_so.chung_tu_dinh_kem = [x for x in co_so.chung_tu_dinh_kem if x["url"] not in request.form.getlist("delete_dinh_kem_anh_chan_dung[]")]
            
                
                
        noi_dung_thuc_hanh:list = json.loads(request.form["noi_dung_thuc_hanh"])
        if co_so.noi_dung_thuc_hanh :
            co_so.noi_dung_thuc_hanh.extend(noi_dung_thuc_hanh) 
        else: co_so.noi_dung_thuc_hanh = noi_dung_thuc_hanh
        db.session.add(co_so)
        db.session.commit()
        return {"msg": "Tạo thành công", "results": schema.dump(co_so)}, HttpCode.Created
class CoSoThucHanhById(Resource):

    @jwt_required()
    def put(self, id):

        schema = CoSoThucHanhSchema(partial=True)
        co_so_thuc_hanh = CoSoThucHanh.query.filter(CoSoThucHanh.id == id).first()
        if co_so_thuc_hanh is None:
            return {"errors": "No data"},  HttpCode.InternalError

        req = {
            "ma_co_so": request.form.get('ma_co_so',None) or None,
            "ten_co_so": request.form.get('ten_co_so',None) or None,
            "giay_chung_nhan": request.form.get('giay_chung_nhan',None) or None,
            "tu_ngay":request.form.get('tu_ngay',None) or None,
            "den_ngay":request.form.get('den_ngay',None) or None,
            "dia_chi_co_so": request.form.get('dia_chi_co_so',None) or None,
            "ten_nguoi_phu_trach": request.form.get('ten_nguoi_phu_trach',None) or None,
            "dien_thoai_nguoi_phu_trach": request.form.get('dien_thoai_nguoi_phu_trach',None) or None,
            "noi_dung_khac": request.form.get('noi_dung_khac',None) or None,
            "so_nha": request.form.get('so_nha',None) or None,
            "quan_huyen_id": request.form.get('quan_huyen_id',None) or None,
            "tinh_thanh_id": request.form.get('tinh_thanh_id',None) or None,
            "xa_phuong_id": request.form.get('xa_phuong_id',None) or None,

        }
        try:
            co_so:CoSoThucHanh = schema.load(req,instance=co_so_thuc_hanh)
            co_so.nhan_vien_id = current_user.id
            
            if request.form.get('xa_phuong_id') is None:
                co_so.xa_phuong = None
                co_so.xa_phuong_id = None

            db.session.add(co_so)
            db.session.flush()
        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest
        
        chung_tu_dinh_kem = request.files.getlist('chung_tu_dinh_kem[]') if "chung_tu_dinh_kem[]" in request.files else None
        upload_errors = []
        chung_tu_dinh_kem = request.files.getlist('chung_tu_dinh_kem[]')
        if chung_tu_dinh_kem and len(chung_tu_dinh_kem) > 0:
            danh_sach_chung_tu_dk,errors = UploadMinio.upload_duocsi(chung_tu_dinh_kem, many=True)
            co_so.chung_tu_dinh_kem.extend(danh_sach_chung_tu_dk)
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_anh_chan_dung[]"):
            co_so.chung_tu_dinh_kem = [x for x in co_so.chung_tu_dinh_kem if x["url"] not in request.form.getlist("delete_dinh_kem_anh_chan_dung[]")]
        
        if co_so.noi_dung_thuc_hanh and request.form.get("noi_dung_thuc_hanh"):
            co_so.noi_dung_thuc_hanh = json.loads(request.form.get("noi_dung_thuc_hanh"))
            
        db.session.commit()
        return {"msg": "Cập nhật thành công", "results": schema.dump(co_so)}, HttpCode.OK
    @jwt_required()
    def delete(self, id):
        schema = CoSoThucHanhSchema()
        co_so = CoSoThucHanh.query.filter(CoSoThucHanh.id == id).first()
        if co_so is None:
            return {"errors": "No data"},  HttpCode.InternalError
        db.session.delete(co_so)
        db.session.commit()

        return  {"msg": "Xóa thành công"}, HttpCode.OK
class CoSoThucHanhGetList(Resource):
    @jwt_required()
    def post(self):
        schema = CoSoThucHanhSchema(many =True) 
        id = request.json.get("nhan_vien_id")
        query = CoSoThucHanh.query.filter(CoSoThucHanh.nhan_vien_id == id)
                # if "id" in request.json:
        #     query = CoSoThucHanh.query.filter(CoSoThucHanh.id == id)
        query = query.order_by(CoSoThucHanh.updated_at.desc()) 
        res = paginate(query,schema)
        return res, HttpCode.OK
    
    