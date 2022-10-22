

from functools import partial
from flask_restful import Resource
from flask import request
from application.extensions import db, pwd_context
from application.commons.pagination import paginate
from application.models.gps import LOAIMAGPS
from application.schemas.gps import GPSSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from flask_jwt_extended import (    
    jwt_required
)
class GPSResource(Resource):
    @jwt_required()
    def post(self):
        schema = GPSSchema()
        gps = schema.load(request.json)
        db.session.add(gps)
        db.session.commit()
        return  schema.dump(gps)
class GPSById(Resource):
    @jwt_required()
    def put(self, id):
        schema = GPSSchema(partial = True)
        gps: LOAIMAGPS= LOAIMAGPS.query.filter(LOAIMAGPS.id == id).first()
     
        if gps is None:
            return {"msg": "không có dữ liệu"}, HttpCode.NotFound
        gps = schema.load(request.json, instance= gps)
        ten = request.json.get('ten')
        if ten is not None:
            gps.ten_khong_dau = clean_string(ten)
        db.session.commit()
        return {"msg": "sửa thành công!",
                "vaitro":schema.dump(gps)}, HttpCode.OK,
       
    @jwt_required()
    def delete(self, id):
        schema = GPSSchema()
        gps: LOAIMAGPS = LOAIMAGPS.query.filter(LOAIMAGPS.id == id).first_or_404()
        db.session.delete(gps)
        db.session.commit()
        return {"msg": "Xóa thành công"}, HttpCode.OK
class GPSGetList(Resource):
    @jwt_required()
    def post(self):
        schema = GPSSchema(many =True)
        query = LOAIMAGPS.query        
        data = request.json  
        if not data:
            query = query.order_by(LOAIMAGPS.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_ten"):
            search_ten = data["search_ten"]
            query = query.filter(LOAIMAGPS.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(LOAIMAGPS.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có tên gps này!"
            }, HttpCode.OK
        
        return res, HttpCode.OK
        












