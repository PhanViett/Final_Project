

from flask_restful import Resource
from flask import request
from application.extensions import db, pwd_context
from application.models.danhmuc_thanh_phan_ho_so import ThanhPhanHoSo
from application.commons.pagination import paginate
from application.models.user import User
from application.utils.helper.string_processing_helper import clean_string
from application.utils.validate.uuid_validator import is_valid_uuid

from application.utils.resource.http_code import HttpCode

from flask_jwt_extended import (    
    jwt_required,
    current_user as user_jwt,
)

from application.schemas.danhmuc_thanh_phan_ho_so import ThanhPhanHoSoSchema

class ThanhPhanHoSoResource(Resource):
    @jwt_required()
    def post(self):
        id = user_jwt.id
        user = User.query.filter(User.id == id).first()
        user.assigned_role
        if "admin" in [x.ten_en for x in user.assigned_role]:
            schema = ThanhPhanHoSoSchema()
            thanhphanhoso = schema.load(request.json)
            db.session.add(thanhphanhoso)
            db.session.commit()
            return  schema.dump(thanhphanhoso)
        else:
            return {"errorCode": "EC18", "msg": "Admin mới có quyền thêm!"}, HttpCode.BadRequest
class ThanhPhanHoSoGetList(Resource):
    @jwt_required()
    def post(self):
        schema = ThanhPhanHoSoSchema(many =True)
        query = ThanhPhanHoSo.query        
        data = request.json  
        if not data:
            query = query.order_by(ThanhPhanHoSo.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_ten", None):
            search_ten = data["search_ten"]
            query = query.filter(ThanhPhanHoSo.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(ThanhPhanHoSo.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có thành phần hồ sơ! "
            }, HttpCode.OK
        return res, HttpCode.OK
    
class ThanhPhanHoSoById(Resource):
    @jwt_required()
    def put(self, id):
        schema = ThanhPhanHoSoSchema()
        thanhphanhoso: ThanhPhanHoSo = ThanhPhanHoSo.query.filter(ThanhPhanHoSo.id == id).first_or_404()
        ten = request.json.get('ten')
        if ten is not None:
            thanhphanhoso.ten_khong_dau =clean_string(ten)
        thanhphanhoso = schema.load(request.json, instance= thanhphanhoso)
        db.session.commit()
        return {"msg": "Sửa thành công",
                  "result": schema.dump(thanhphanhoso)} 


    @jwt_required()
    def get(self,id):
        schema = ThanhPhanHoSoSchema()
        thanhphanhoso: ThanhPhanHoSo = ThanhPhanHoSo.query.filter(ThanhPhanHoSo.id == id).first_or_404()
        return schema.dump(thanhphanhoso)
    @jwt_required()
    def delete(self, id):
        schema = ThanhPhanHoSoSchema()
        thanhphanhoso: ThanhPhanHoSo = ThanhPhanHoSo.query.filter(ThanhPhanHoSo.id == id).first_or_404()
        db.session.delete(thanhphanhoso)
        db.session.commit()
        return {"msg": "xóa thành công!"}, HttpCode.OK
    

             

        












