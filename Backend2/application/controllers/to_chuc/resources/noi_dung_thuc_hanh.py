

from functools import partial
from flask_restful import Resource
from flask import request
from application.extensions import db, pwd_context
from application.commons.pagination import paginate
from application.models.noi_dung_thuc_hanh import NoiDungThucHanh
from application.schemas.noi_dung_thuc_hanh import NoiDungThucHanhSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from flask_jwt_extended import (    
    jwt_required
)
class NoiDungThucHanhResource(Resource):
    @jwt_required()
    def post(self):
        schema = NoiDungThucHanhSchema()
        gps = schema.load(request.json)
        db.session.add(gps)
        db.session.commit()
        return {"msg": "Tạo thành công!",
                "gps":schema.dump(gps)}, HttpCode.OK,

class NoiDungThucHanhById(Resource):
    @jwt_required()
    def put(self, id):
        schema = NoiDungThucHanhSchema(partial = True)
        noi_dung_thuc_hanh: NoiDungThucHanh= NoiDungThucHanh.query.filter(NoiDungThucHanh.id == id).first()
     
        if noi_dung_thuc_hanh is None:
            return {"msg": "không có dữ liệu"}, HttpCode.NotFound
        chung_chi = schema.load(request.json, instance= noi_dung_thuc_hanh)
        ten = request.json.get('ten')
        if ten is not None:
            chung_chi.ten_khong_dau = clean_string(ten)
        db.session.commit()
        return {"msg": "sửa thành công!",
                "vaitro":schema.dump(chung_chi)}, HttpCode.OK,
       
    @jwt_required()
    def delete(self, id):
        schema = NoiDungThucHanhSchema()
        noi_dung_thuc_hanh: NoiDungThucHanh = NoiDungThucHanh.query.filter(NoiDungThucHanh.id == id).first_or_404()
        db.session.delete(noi_dung_thuc_hanh)
        db.session.commit()
        return {"msg": "Xóa thành công"}, HttpCode.OK
class NoiDungThucHanhGetList(Resource):
    @jwt_required()
    def post(self):
        schema = NoiDungThucHanhSchema(many =True)
        query = NoiDungThucHanh.query        
        data = request.json  
        if not data:
            query = query.order_by(NoiDungThucHanh.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_ten", None):
            search_ten = data["search_ten"]
            query = query.filter(NoiDungThucHanh.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(NoiDungThucHanh.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có nội dung thực hàng!"
            }, HttpCode.OKs
        return res, HttpCode.OK
        












