

from functools import partial
from flask_restful import Resource
from flask import request
from application.extensions import db, pwd_context
from application.commons.pagination import paginate
from application.models.loai_ma_chung_chi import LOAIMACHUNGCHI
from application.schemas.loai_ma_chung_chi import LoaiMaChungChichema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from flask_jwt_extended import (    
    jwt_required
)
from application.extensions import redisdb
class LoaiMaChungChiResource(Resource):
    @jwt_required()
    def post(self):
        schema = LoaiMaChungChichema()
        gps = schema.load(request.json)
        db.session.add(gps)
        db.session.commit()
        return {"msg": "Tạo thành công!",
                "gps":schema.dump(gps)}, HttpCode.OK,

class LoaiMaChungChiById(Resource):
    @jwt_required()
    def put(self, id):
        schema = LoaiMaChungChichema(partial = True)
        chung_chi: LOAIMACHUNGCHI= LOAIMACHUNGCHI.query.filter(LOAIMACHUNGCHI.id == id).first()
     
        if chung_chi is None:
            return {"msg": "không có dữ liệu"}, HttpCode.NotFound
        chung_chi = schema.load(request.json, instance= chung_chi)
        ten = request.json.get('ten')
        if ten is not None:
            chung_chi.ten_khong_dau = clean_string(ten)
        db.session.commit()
        return {"msg": "sửa thành công!",
                "vaitro":schema.dump(chung_chi)}, HttpCode.OK,
       
    @jwt_required()
    def delete(self, id):
        schema = LoaiMaChungChichema()
        gps: LOAIMACHUNGCHI = LOAIMACHUNGCHI.query.filter(LOAIMACHUNGCHI.id == id).first_or_404()
        db.session.delete(gps)
        db.session.commit()
        return {"msg": "Xóa thành công"}, HttpCode.OK
class LoaiMaChungChiGetList(Resource):
    @jwt_required()
    def post(self):
        schema = LoaiMaChungChichema(many =True)
        query = LOAIMACHUNGCHI.query        
        data = request.json  
        if not data:
            query = query.order_by(LOAIMACHUNGCHI.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_ten", None):
            search_ten = data["search_ten"]
            query = query.filter(LOAIMACHUNGCHI.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(LOAIMACHUNGCHI.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có loại mã chứng chỉ! "
            }, HttpCode.OK
        return res, HttpCode.OK

class FilterByDoiTuong(Resource):
    @jwt_required()
    def get(self, doi_tuong_id):
        query = LOAIMACHUNGCHI.query.filter(LOAIMACHUNGCHI.doi_tuong == doi_tuong_id)       
        chung_chis = []
        for chung_chi in query:
            chung_chis.append(
                {
                    "label": chung_chi.ma_chung_chi,
                    "value": str(chung_chi.id),
                }
            )

        return {
            "results": chung_chis 
        }, HttpCode.OK

class GetDetail(Resource):
    @jwt_required()
    def get(self, id):
        schema = LoaiMaChungChichema()
        query = LOAIMACHUNGCHI.query.filter(LOAIMACHUNGCHI.id == id).first()
        p = redisdb
        if p.get(str(query.id)) is None:
            p.set(str(query.id), query.so_da_cap)
        setattr(query, 'so_da_cap', int(p.get(str(query.id))) + 1)
        return schema.dump(query), HttpCode.OK












