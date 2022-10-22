

from flask_restful import Resource
from flask import request
from application.extensions import db, pwd_context
from application.models.danhmuc_noi_tot_nghiep import NoiTotNghiep
from application.commons.pagination import paginate
from application.models.user import User
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from application.schemas.danhmuc_noi_tot_nghiep import NoiTotNghiepSchema
from flask_jwt_extended import (    
    jwt_required,
    current_user as user_jwt,
)

from application.utils.validate.uuid_validator import is_valid_uuid


# ok//
class NoiTotNghiepResource(Resource):
    @jwt_required()
    def post(self):
        id = user_jwt.id
        user = User.query.filter(User.id == user_jwt.id).first()
        user.assigned_role
        
        if "admin" in [x.ten_en for x in user.assigned_role]:
            schema = NoiTotNghiepSchema()
            noitotnghiep = schema.load(request.json)
            db.session.add(noitotnghiep)
            db.session.commit()
            return  schema.dump(noitotnghiep)
        else:
            return {"errorCode":"EC18","msg":"Admin mới có quyền thêm!"},HttpCode.BadRequest

# oke
class NoiTotNghiepGetList(Resource):
    @jwt_required()
    def post(self):
        schema = NoiTotNghiepSchema(many =True)
        query = NoiTotNghiep.query        
        data = request.json  
        if not data:
            query = query.order_by(NoiTotNghiep.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_ten", None):
            search_ten = data["search_ten"]
            query = query.filter(NoiTotNghiep.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(NoiTotNghiep.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có nơi tốt nghiệp!"
            }, HttpCode.OK
        return res, HttpCode.OK
    
# oke
class NoiTotNghiepById(Resource):
    @jwt_required()
    
    def put(self, id):
        schema = NoiTotNghiepSchema()
        noitotnghiep: NoiTotNghiep = NoiTotNghiep.query.filter(NoiTotNghiep.id == id).first_or_404()
        ten = request.json.get('ten')
        if ten is not None:
            noitotnghiep.ten_khong_dau = clean_string(ten)
        noitotnghiep = schema.load(request.json, instance= noitotnghiep)
        db.session.commit()
        return schema.dump(noitotnghiep)

# oke
    @jwt_required()
    def get(self,id):
        schema = NoiTotNghiepSchema()
        noitotnghiep: NoiTotNghiep = NoiTotNghiep.query.filter(NoiTotNghiep.id == id).first_or_404()
        return schema.dump(noitotnghiep)
# oke
    
    @jwt_required()
    def delete(self, id):
        schema = NoiTotNghiepSchema()
        noitotnghiep: NoiTotNghiep = NoiTotNghiep.query.filter(NoiTotNghiep.id == id).first_or_404()
        db.session.delete(noitotnghiep)
        db.session.commit()
        return {"msg": "xóa thành công!"}, HttpCode.OK


        












