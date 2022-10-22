from re import L
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError
from application.models.lich_su_chung_chi import LichSuChungChi
from application.schemas.lich_su_chung_chi import LichSuChungChiSchema
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
from application.schemas.bang_cap import BangCapSchema
from datetime import datetime
from application.commons.pagination import paginate


from application.extensions import db
class LichSuChungChiResource(Resource):

    @jwt_required()
    def post(self):
        schema = LichSuChungChiSchema()
        req = {
            "user_id": request.form.get("user_id"),
            "loai_thay_doi": request.form.get("loai_thay_doi"),
            "noi_dung_thay_doi": request.form.get("noi_dung_thay_doi"),
            "chung_chi_cu": request.form.get('chung_chi_cu'),
            "chung_chi_moi": request.form.get('chung_chi_moi'),
            "chuyen_vien_id": request.form.get('chuyen_vien_id'),
            "lanh_dao_id": request.form.get('lanh_dao_id'),
            "so_quyet_dinh": request.form.get('so_quyet_dinh'),

            
            # "trang_thai": request.form.get('trang_thai')
            
            
        }

        try:
            chung_chi = schema.load(req)
            # chung_chi. = current_user.id
            chung_chi.updated_by = current_user.id
            chung_chi.chuyen_vien_id = current_user.id
            chung_chi.lanh_dao_id = current_user.id


            ngay_thay_doi = request.form.get("ngay_thay_doi")
            chung_chi.ngay_thay_doi = ngay_thay_doi
        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest
        
        chung_tu_dinh_kem = request.files.get('chung_tu_dinh_kem')
        try:
            if chung_tu_dinh_kem:
                chung_tu_dinh_kem = UploadMinio.upload_duocsi(chung_tu_dinh_kem)
                chung_chi.chung_tu_dinh_kem = chung_tu_dinh_kem
        except:
            return {"errors": "Tải file thất bại"},  HttpCode.InternalError
        trang_thai = request.form.get('trang_thai')
        if trang_thai == 'True':
            chung_chi.trang_thai = True
        elif trang_thai == 'False':
            chung_chi.trang_thai = False
        

        db.session.add(chung_chi)
        db.session.commit()

        return {"msg": "Tạo thành công", "results": schema.dump(chung_chi)}, HttpCode.Created
class LichSuChungChiById(Resource):

    @jwt_required()
    def put(self, id):

        schema = LichSuChungChiSchema(partial =True)
        chung_chi = LichSuChungChi.query.filter(LichSuChungChi.id == id).first()
        if chung_chi is None:
            return {"errors": "No data"},  HttpCode.InternalError

        req = {
            "user_id": request.form.get("user_id"),
            "loai_thay_doi": request.form.get("loai_thay_doi"),
            "noi_dung_thay_doi": request.form.get("noi_dung_thay_doi"),
            "chung_chi_cu": request.form.get('chung_chi_cu'),
            "chung_chi_moi": request.form.get('chung_chi_moi'),
            "chuyen_vien_id": request.form.get('chuyen_vien_id'),
            "lanh_dao_id": request.form.get('lanh_dao_id'),
            "so_quyet_dinh": request.form.get('so_quyet_dinh'),

        }

        try:
            chung_chi = schema.load(req, instance=chung_chi)
            chung_chi.user_id = current_user.id
            chung_chi.updated_at = db.func.current_timestamp()
            ngay_thay_doi = request.form.get("ngay_thay_doi")
            chung_chi.ngay_thay_doi = ngay_thay_doi

        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest
        
        chung_tu_dinh_kem = request.files.get('chung_tu_dinh_kem')
        try:
            if chung_tu_dinh_kem:
                chung_tu_dinh_kem = UploadMinio.upload_duocsi(chung_tu_dinh_kem)
                chung_chi.chung_tu_dinh_kem = chung_tu_dinh_kem
        except:
            return {"errors": "Tải file thất bại"},  HttpCode.InternalError
        trang_thai = request.form.get('trang_thai')
        
        if trang_thai == 'True':
            chung_chi.trang_thai = True
        elif trang_thai == 'False':
            chung_chi.trang_thai = False
        db.session.commit()

        return {"msg": "Cập nhật thành công", "results": schema.dump(chung_chi)}, HttpCode.OK
    @jwt_required()
    def delete(self, id):
        schema = LichSuChungChiSchema()
        chung_chi = LichSuChungChi.query.filter(LichSuChungChi.id == id).first()
        if chung_chi is None:
                return {"errors": "Không có dữ liệu!"},  HttpCode.InternalError
        db.session.delete(chung_chi)
        db.session.commit()
        
        return {"msg": "xóa thành công!"}, HttpCode.OK
class LichSuChungChiGetList(Resource):
    @jwt_required()
    def post(self):
        schema = LichSuChungChiSchema(many =True)
        user_id  = request.json.get("user_id")
        query = LichSuChungChi.query             
        if not request.json:
            query = query.order_by(LichSuChungChi.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
                
        if "user_id" in request.json:
            query = query.filter(LichSuChungChi.user_id == user_id)
            return paginate(query,schema), HttpCode.OK
               
        # if len(query.all()) <= 0:
        #      return {"msg":"không có id lịch sử chứng chỉ!"}
        return paginate(query,schema), HttpCode.OK
        

