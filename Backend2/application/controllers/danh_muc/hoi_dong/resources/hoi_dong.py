from flask_restful import Resource
from flask import request, jsonify
from application.extensions import db, pwd_context
from application.models.danhmuc_hoi_dong import HoiDong
from application.schemas.danhmuc_hoi_dong import HoiDongSchema
from application.utils.helper.string_processing_helper import clean_string

from application.utils.resource.http_code import HttpCode
from application.commons.pagination import paginate
from application.models import User
from flask_jwt_extended import (    
    jwt_required,
    current_user as user_jwt,
)


class HoiDongResource(Resource):
    @jwt_required()
    def post(self):
        id = user_jwt.id
        user = User.query.filter(User.id == user_jwt.id).first()
        
        if not "admin" in [x.ten_en for x in user.assigned_role]:
            return {"errorCode": "EC18","msg":"Admin mới có quyền thêm!"},HttpCode.BadRequest

        schema = HoiDongSchema()
        hoidong = schema.load(request.json)
        db.session.add(hoidong)
        db.session.commit()
        return   {"msg": "thêm thành công",
                "result": schema.dump(hoidong)  
                }


class HoiDongGetList(Resource):
    @jwt_required()
    def post(self):
        schema = HoiDongSchema(many =True)
        query = HoiDong.query        
        data = request.json  
        if not data:
            query = query.order_by(HoiDong.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_ten", None):
            search_ten = data["search_ten"]
            query = query.filter(HoiDong.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(HoiDong.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có hội đồng "
            }, HttpCode.OK
        return res, HttpCode.OK
    
    

class HoiDongById(Resource):
    @jwt_required()
    def put(self, id):
        schema = HoiDongSchema(partial= True)
        hoidong: HoiDong = HoiDong.query.filter(HoiDong.id == id).first()
        # hoidong.updated_at = db.func.current_timestamp()
        ten = request.json.get('ten_hoi_dong')
        if ten is not None:
            hoidong.ten_khong_dau = clean_string(ten)
        if hoidong is None:
            return {"msg": "danh muc ko ton tai"}, HttpCode.BadRequest
        hoidong = schema.load(request.json, instance=hoidong)
        db.session.commit()
        return  {
            "msg": "Sửa thành công",
            "result": schema.dump(hoidong)  
        }
    @jwt_required()
    def get(self,id):
        schema = HoiDongSchema()
        hoidong: HoiDong = HoiDong.query.filter(HoiDong.id == id).first_or_404()
        return schema.dump(hoidong)
    @jwt_required()
    def delete(self, id):
        schema = HoiDongSchema()
        hoidong: HoiDong = HoiDong.query.filter(HoiDong.id == id).first_or_404()
        db.session.delete(hoidong)
        db.session.commit()
        return {"msg": "xóa thành công!"}, HttpCode.OK

       

        












