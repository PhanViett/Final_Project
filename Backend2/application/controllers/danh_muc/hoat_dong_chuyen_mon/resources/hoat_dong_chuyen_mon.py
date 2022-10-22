

import uuid
from flask_restful import Resource
from flask import request
from application.extensions import db, pwd_context
from application.models.danhmuc_pham_vi_hoat_dong_chuyen_mon import PhamViHoatDongChuyenMon
from application.models.danhmuc_pham_vi_hoat_dong_kinh_doanh import PhamViHoatDongKinhDoanh
from application.commons.pagination import paginate
from application.models.user import User
from application.schemas.danhmuc_pham_vi_hoat_dong_chuyen_mon import PhamViHoatDongChuyenMonSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from flask_jwt_extended import (    
    jwt_required,
    current_user as user_jwt,
)

class PhamViHoatDongChuyenMonResource(Resource):
    @jwt_required()
    def post(self):
        id = user_jwt.id
        user = User.query.filter(User.id == user_jwt.id).first()
        user.assigned_role
        
        if "admin" in [x.ten_en for x in  user.assigned_role]:
            schema = PhamViHoatDongChuyenMonSchema()
            phamvihoatdongchuyenmon = schema.load(request.json)
            db.session.add(phamvihoatdongchuyenmon)
            db.session.commit()
            return {
                "msg":"Thêm thành công!",
                "result": schema.dump(phamvihoatdongchuyenmon) 
                } 
        else:
            return {"errorCode":"EC18","msg":"Admin mới có quyền thêm!"},HttpCode.BadRequest

class PhamViHoatDongChuyenMonGetList(Resource):
    @jwt_required()
    def post(self):
        schema = PhamViHoatDongChuyenMonSchema(many =True)
        query = PhamViHoatDongChuyenMon.query        
        data = request.json  
        if not data:
            query = query.order_by(PhamViHoatDongChuyenMon.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_ten", None):
            search_ten = data["search_ten"]
            query = query.filter(PhamViHoatDongChuyenMon.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(PhamViHoatDongChuyenMon.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có hoạt động chuyên môn! "
            }, HttpCode.OK
        return res, HttpCode.OK
    
class PhamViHoatDongChuyenMonById(Resource):
    @jwt_required()
    def put(self, id):
        schema = PhamViHoatDongChuyenMonSchema(partial= True)
        phamvihoatdongchuyenmon: PhamViHoatDongChuyenMon = PhamViHoatDongChuyenMon.query.filter(PhamViHoatDongChuyenMon.id == id).first()
        ten = request.json.get('ten')
        if ten is not None:
            phamvihoatdongchuyenmon.ten_khong_dau = clean_string(ten)
        phamvihoatdongchuyenmon = schema.load(request.json, instance= phamvihoatdongchuyenmon)
        
        db.session.commit()
        
        return  {"msg": "Sửa thành công",
                  "result": schema.dump(phamvihoatdongchuyenmon)}
    
    @jwt_required()
    def delete(self, id):
        schema = PhamViHoatDongChuyenMonSchema()
        phamvihoatdongchuyenmon: PhamViHoatDongChuyenMon = PhamViHoatDongChuyenMon.query.filter(PhamViHoatDongChuyenMon.id == id).first_or_404()
        db.session.delete(phamvihoatdongchuyenmon)
        db.session.commit()
        return {"msg": "xóa thành công!"}, HttpCode.OK


        












