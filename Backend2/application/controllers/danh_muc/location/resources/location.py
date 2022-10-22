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




from application.schemas.tinh_thanh import TinhThanhSchema

# get all tinh thanh    
class GetTinhThanh(Resource):
    @jwt_required()
    def get(self):
        schema = TinhThanhSchema(many =True)
        tinhthanh = TinhThanh.query
        return paginate(tinhthanh,schema)
class TinhThanhById(Resource):
#     def put(self, id):
#         schema = TinhThanhSchema()
#         tinhthanh: TinhThanh = TinhThanh.query.filter(TinhThanh.id == id).first()
#         # if hoidong is None:
#         #     return {"msg": "danh muc ko ton tai"}, HttpCode.BadRequest
#         tinhthanh = schema.load(request.json, instance=tinhthanh)
#         db.session.commit()
#         return schema.dump(tinhthanh)
    @jwt_required()
    def get(self,id):
        schema = TinhThanhSchema()
        tinhthanh: TinhThanh = TinhThanh.query.filter(TinhThanh.id == id).first_or_404()
        return schema.dump(tinhthanh)
# class QuanHuyenById(Resource):
#      def get(self,id):
#         schema = QuanHuyenSchema()
#         quanhuyen: QuanHuyen = QuanHuyen.query.filter(QuanHuyen.id == id).first_or_404()
#         return schema.dump(quanhuyen)
    

    # def delete(self, id):
    #     schema = HoiDongSchema()
    #     hoidong: HoiDong = HoiDong.query.filter(HoiDong.id == id).first_or_404()
    #     db.session.delete(hoidong)
    #     db.session.commit()
    #     return {"msg": "danh_muc deleted"}, HttpCode.OK
  
