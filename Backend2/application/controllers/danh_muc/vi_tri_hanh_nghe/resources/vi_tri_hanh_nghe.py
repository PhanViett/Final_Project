

from flask_restful import Resource
from flask import request
from application.extensions import db, pwd_context
from application.commons.pagination import paginate
from application.models.danhmuc_vi_tri_hanh_nghe import ViTriHanhNghe
from application.models.user import User
from application.schemas.danhmuc_vi_tri_hanh_nghe import ViTriHanhNgheSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from flask_jwt_extended import (    
    jwt_required,
    current_user as user_jwt,
)

from application.utils.validate.uuid_validator import is_valid_uuid
# ok//
class ViTriHanhNgheResource(Resource):
    @jwt_required()
    def post(self):
        id = user_jwt.id
        user = User.query.filter(User.id == user_jwt.id).first()
        user.assigned_role
        
        if "admin" in [x.ten_en for x in user.assigned_role]:
            schema = ViTriHanhNgheSchema()
            vitrihanhnghe = schema.load(request.json)
            db.session.add(vitrihanhnghe)
            db.session.commit()
            return  schema.dump(vitrihanhnghe)
        else:
            return {"errorCode":"EC18","msg":"Admin mới có quyền thêm!"},HttpCode.BadRequest
# oke
class ViTriHanhNgheGetList(Resource):
    @jwt_required()
    def post(self):
        schema = ViTriHanhNgheSchema(many =True)
        query = ViTriHanhNghe.query        
        data = request.json  
        if not data:
            query = query.order_by(ViTriHanhNghe.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_ten", None):
            search_ten = data["search_ten"]
            query = query.filter(ViTriHanhNghe.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(ViTriHanhNghe.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có vị trí hành nghề!"
            }, HttpCode.OK
        return res, HttpCode.OK
    
# oke
class ViTriHanhNgheById(Resource):
    @jwt_required()
    def put(self, id):
        schema = ViTriHanhNgheSchema()
        vitrihanhnghe: ViTriHanhNghe= ViTriHanhNghe.query.filter(ViTriHanhNghe.id == id).first()
        ten = request.json.get('ten')
        if ten is not None:
            vitrihanhnghe.ten_khong_dau =clean_string(ten)
        if vitrihanhnghe is None:
            return {"msg": "không có dữ liệu"}, HttpCode.NotFound
        vitrihanhnghe = schema.load(request.json, instance= vitrihanhnghe)
        db.session.commit()
        return {"msg": "có dữ liệu",
                "vitrihanhnghe":schema.dump(vitrihanhnghe)}, HttpCode.OK,

# oke
    @jwt_required()
    def get(self,id):
        schema = ViTriHanhNgheSchema()
        vitrihanhnghe: ViTriHanhNghe = ViTriHanhNghe.query.filter(ViTriHanhNghe.id == id).first_or_404()
        return schema.dump(vitrihanhnghe)
# oke
    @jwt_required()
    def delete(self, id):
        schema = ViTriHanhNgheSchema()
        vitrihanhnghe: ViTriHanhNghe = ViTriHanhNghe.query.filter(ViTriHanhNghe.id == id).first_or_404()
        db.session.delete(vitrihanhnghe)
        db.session.commit()
        return {"msg": "Xóa thành công"}, HttpCode.OK
  
        












