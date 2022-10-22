
from flask_restful import Resource
from flask import request, jsonify
from application.extensions import db, pwd_context
from application.models.danhmuc_loai_hinh_kinh_doanh import LoaiHinhKinhDoanh
from application.utils.validate.uuid_validator import is_valid_uuid
from application.schemas.danhmuc_loai_hình_kinh_doanh import LoaiHinhKinhDoanhSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from application.commons.pagination import paginate
from application.models import User
from flask_jwt_extended import (    
    jwt_required,
    current_user as user_jwt,
    
)

class LoaiHinhKinhDoanhResource(Resource):
    @jwt_required()
    def post(self):
        id = user_jwt.id
        user = User.query.filter(User.id == id).first()
        user.assigned_role 

        if "admin" in [x.ten_en for x in user.assigned_role]:
              
            schema = LoaiHinhKinhDoanhSchema()
            loaihinhkinhdoanh = schema.load(request.json)
            db.session.add(loaihinhkinhdoanh)
            db.session.commit()
            return  schema.dump(loaihinhkinhdoanh)   
        else:
            return {"errorCode": "EC18", "msg": "Admin mới có quyền thêm!"}, HttpCode.BadRequest
        


class LoaiHinhKinhDoanhGetList(Resource):
    @jwt_required()
    def post(self):
        schema = LoaiHinhKinhDoanhSchema(many =True)
        query = LoaiHinhKinhDoanh.query        
        data = request.json  
        if not data:
            query = query.order_by(LoaiHinhKinhDoanh.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_ten", None):
            search_ten = data["search_ten"]
            query = query.filter(LoaiHinhKinhDoanh.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(LoaiHinhKinhDoanh.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có loại hình kinh doanh! "
            }, HttpCode.OK
        return res, HttpCode.OK

class LoaiHinhKinhDoanhById(Resource):
    @jwt_required()
    
    def put(self, id):
        schema = LoaiHinhKinhDoanhSchema()
        loaihinhkinhdoanh: LoaiHinhKinhDoanh = LoaiHinhKinhDoanh.query.filter(LoaiHinhKinhDoanh.id == id).first()
        ten = request.json.get('ten')
        if ten is not None:
            loaihinhkinhdoanh.ten_khong_dau = clean_string(ten)
        if loaihinhkinhdoanh is None:
            return {"msg": "loại hình kinh doanh không tồn tại!"}, HttpCode.BadRequest
        loaihinhkinhdoanh = schema.load(request.json, instance=loaihinhkinhdoanh)
        db.session.commit()
        return schema.dump(loaihinhkinhdoanh)
    @jwt_required()

    def get(self,id):
        schema = LoaiHinhKinhDoanhSchema()
        loaihinhkinhdoanh: LoaiHinhKinhDoanh = LoaiHinhKinhDoanh.query.filter(LoaiHinhKinhDoanh.id == id).first_or_404()
        return schema.dump(loaihinhkinhdoanh)
    @jwt_required()

    def delete(self, id):
        schema = LoaiHinhKinhDoanhSchema()
        loaihinhkinhdoanh: LoaiHinhKinhDoanh = LoaiHinhKinhDoanh.query.filter(LoaiHinhKinhDoanh.id == id).first_or_404()
        db.session.delete(loaihinhkinhdoanh)
        db.session.commit()
        return {"msg": "xóa thành công"}, HttpCode.OK
   

        

    










