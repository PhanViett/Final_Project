
from datetime import datetime
from functools import partial
from re import L
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError
from application.models.bang_cap import BangCap
from application.models.chung_nhan_thuc_hanh_co_so import ChungNhanCoSo
from application.models.user import User
from application.schemas.chung_nhan_thuc_hanh_co_so import ChungNhanCoSoSchema
from application.utils.helper.convert_timestamp_helper import convert_timestamp
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
from application.extensions import db
from application.commons.pagination import paginate
from application.utils.validate.uuid_validator import is_valid_uuid
from application.utils.helper.string_processing_helper import clean_string


class ThucHanhCoSoResource(Resource):
#add oke
    @jwt_required()
    def post(self):
        schema = ChungNhanCoSoSchema()
        req = {
            "so_giaychungnhan": request.form.get("so_giaychungnhan"),
            "diachi": request.form.get('diachi'),
            "quan_huyen_id": request.form.get('quan_huyen_id'),
            "tinh_thanh_id": request.form.get('tinh_thanh_id'),
            "xa_phuong_id": request.form.get('xa_phuong_id'),
            "coso_kinhdoanh_id": request.form.get('coso_kinhdoanh_id'),
            
        }
        try:
            thuc_hanh:ChungNhanCoSo = schema.load(req)
            thuc_hanh.created_by = current_user.id
            ngay_kiemtra = request.form.get("ngay_kiemtra")
            thuc_hanh.ngay_kiemtra = ngay_kiemtra
            ngay_cap = request.form.get("ngay_cap")
            thuc_hanh.ngay_cap = ngay_cap
            ngay_hieu_luc = request.form.get("ngay_hieu_luc")
            thuc_hanh.ngay_hieu_luc = ngay_hieu_luc
            ngay_het_han = request.form.get("ngay_het_han")
            thuc_hanh.ngay_het_han = ngay_het_han
        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest
        
        dinhkem_giaychungnhan = request.files.get('dinhkem_giaychungnhan')
        try:
            if dinhkem_giaychungnhan:
                dinhkem_giaychungnhan = UploadMinio.upload_duocsi(dinhkem_giaychungnhan)
                thuc_hanh.dinhkem_giaychungnhan = dinhkem_giaychungnhan
        except:
            return {"errors": "Tải file thất bại"},  HttpCode.InternalError
        
    
        trang_thai = request.form.get('trang_thai')
        if trang_thai == 'True':
            thuc_hanh.trang_thai = True

        db.session.add(thuc_hanh)
        db.session.commit()

        return {"msg": "Tạo thành công", "results": schema.dump(thuc_hanh)}, HttpCode.Created
  

    
        


class ChungNhanCoSoById(Resource):
    @jwt_required()
    def put(self, id):
        schema = ChungNhanCoSoSchema(partial =True)
        chung_nhan = ChungNhanCoSo.query.filter(ChungNhanCoSo.id == id).first()
        if chung_nhan is None:
            return {"errors": "No data"},  HttpCode.InternalError
        req = {
            "so_giaychungnhan": request.form.get("so_giaychungnhan"),
            "diachi": request.form.get('diachi'),
            # "ngay_kiemtra": request.form.get('ngay_kiemtra'),
            # "ngay_cap": request.form.get('ngay_cap'),
            # "ngay_hieu_luc": request.form.get('ngay_hieu_luc'),
            # "ngay_het_han": request.form.get('ngay_het_han'),


            "quan_huyen_id": request.form.get('quan_huyen_id'),
            "tinh_thanh_id": request.form.get('tinh_thanh_id'),
            "xa_phuong_id": request.form.get('xa_phuong_id'),
            "coso_kinhdoanh_id": request.form.get('coso_kinhdoanh_id'),
            
        }
        try:
            thuc_hanh = schema.load(req,instance=chung_nhan)
            thuc_hanh.created_by = current_user.id
            ngay_kiemtra = request.form.get("ngay_kiemtra")
            thuc_hanh.ngay_kiemtra = ngay_kiemtra
            ngay_cap = request.form.get("ngay_cap")
            thuc_hanh.ngay_cap = ngay_cap
            ngay_hieu_luc = request.form.get("ngay_hieu_luc")
            thuc_hanh.ngay_hieu_luc = ngay_hieu_luc
            ngay_het_han = request.form.get("ngay_het_han")
            thuc_hanh.ngay_het_han = ngay_het_han
        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest
        
        # dinh_kem = request.files['dinhkem_giaychungnhan'] if "dinhkem_giaychungnhan" in request.files else None
        # if dinh_kem:
        #         try:
        #                 dinhkem_giaychungnhan = UploadMinio.upload_duocsi(dinhkem_giaychungnhan)
        #                 thuc_hanh.dinhkem_giaychungnhan = dinhkem_giaychungnhan
        #         except:
        #             return {"errors": "Tải file thất bại"},  HttpCode.InternalError
        dinhkem_giaychungnhan = request.files.get('dinhkem_giaychungnhan')
        try:
            if dinhkem_giaychungnhan:
                dinhkem_giaychungnhan = UploadMinio.upload_duocsi(dinhkem_giaychungnhan)
                thuc_hanh.dinhkem_giaychungnhan = dinhkem_giaychungnhan
        except:
            return {"errors": "Tải file thất bại"},  HttpCode.InternalError
    
        trang_thai = request.form.get('trang_thai')
        if trang_thai == 'True':
            thuc_hanh.trang_thai = True

        db.session.commit()

        return {"msg": "Cập nhật thành công", "results": schema.dump(thuc_hanh)}, HttpCode.Created
    @jwt_required()
    def delete(self, id):
        schema = ChungNhanCoSoSchema()
        chung_nhan = ChungNhanCoSo.query.filter(ChungNhanCoSo.id == id).first()
        if chung_nhan is None:
                return {"errors": "Không có dữ liệu!"},  HttpCode.InternalError
        db.session.delete(chung_nhan)
        db.session.commit()
        
        return {"msg": "xóa thành công!"}, HttpCode.OK
        
class ThucHanhCoSoGetList(Resource):
    @jwt_required()
    def post(self):
        schema = ChungNhanCoSoSchema(many =True)
        query = ChungNhanCoSo.query        
        data = request.json  
        if not data:
            query = query.order_by(ChungNhanCoSo.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_so_giaychungnhan", None):
            search_so_giaychungnhan = data["search_so_giaychungnhan"]
            query = query.filter(ChungNhanCoSo.so_giaychungnhan.like(f"%{search_so_giaychungnhan}%"))
            
              
        query = query.order_by(ChungNhanCoSo.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có chứng nhận thực hành cơ sở! "
            }, HttpCode.OK
        return res, HttpCode.OK
class TimKiemTheoSoGiayChungNhan(Resource):
    @jwt_required()
    def post(self):
        schema = ChungNhanCoSoSchema(many =True)
        so_giaychungnhan = request.json.get("so_giaychungnhan")
        query = ChungNhanCoSo.query.order_by(ChungNhanCoSo.updated_at.desc())         
        # # if not request.json:
        #     query = query.order_by(ChungNhanCoSo.updated_at.desc())
        #     return paginate(query, schema), HttpCode.OK
        

        # if "trang_thai" in request.json:
        #     if request.json.get("trang_thai") != None:
        #         query = query.filter(
        #             NoiTotNghiep.trang_thai == request.json.get("trang_thai")
        #         )  
        if "so_giaychungnhan" in request.json:
            query = query.filter(ChungNhanCoSo.so_giaychungnhan == so_giaychungnhan )     
        if len(query.all()) <= 0:
             return {"msg":"chứng nhận không có!",
                     "results": schema.dump(query)}, HttpCode.OK
        return paginate(query,schema), HttpCode.OK
        