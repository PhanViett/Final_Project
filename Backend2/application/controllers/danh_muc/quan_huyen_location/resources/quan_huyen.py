from flask_restful import Resource
from flask import request
from application.extensions import db, pwd_context
from application.models.quan_huyen import QuanHuyen
from application.models.tinh_thanh import TinhThanh
from application.commons.pagination import paginate
from application.schemas.quan_huyen import QuanHuyenSchema
from flask_jwt_extended import (    
    jwt_required
)
class GetQuanHuyen(Resource):
    @jwt_required()
    def get(self):
        schema = QuanHuyenSchema(many =True)
        quanhuyen = QuanHuyen.query
        return paginate(quanhuyen,schema)
    

class GetQuanHuyenByTinhThanhID(Resource):
    @jwt_required()
    def get(self, id):
        schema = QuanHuyenSchema(many =True)
        quanhuyen = QuanHuyen.query.filter(QuanHuyen.tinhthanh_id == id)
        return paginate(quanhuyen,schema)
class QuanHuyenById(Resource):
     @jwt_required()
     def get(self,id):
        schema = QuanHuyenSchema()
        quanhuyen: QuanHuyen = QuanHuyen.query.filter(QuanHuyen.id == id).first_or_404()
        return schema.dump(quanhuyen)
    

    
  
