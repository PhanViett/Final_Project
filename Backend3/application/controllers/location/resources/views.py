from flask_restful import Resource
from flask_jwt_extended import jwt_required
from application.models import TinhThanh
from application.schemas.tinh_thanh import TinhThanhDisplayCMNDSchema, TinhThanhSchema
from application.models import QuanHuyen
from application.schemas.quan_huyen import QuanHuyenSchema
from application.models import XaPhuong
from application.schemas.xa_phuong import XaPhuongSchema


class TinhThanhGetAll(Resource):
    @jwt_required()
    def get(self):
        schema = TinhThanhSchema(many=True)
        query = TinhThanh.query.filter(TinhThanh.loai == 0).all()
        return {
            "msg": "Thành công",
            "results":
            schema.dump(query)
        }


class QuanHuyenGetAll(Resource):
    @jwt_required()
    def get(self):
        schema = QuanHuyenSchema(many=True)
        query = QuanHuyen.query.filter(QuanHuyen.active == "1").all()
        return {
            "msg":"Thành công",
            "results":schema.dump(query)
        }

class QuanHuyenGetById(Resource):
    @jwt_required()
    def get(self, tinh_thanh_id):
        schema = QuanHuyenSchema(many=True)
        query = QuanHuyen.query.filter(QuanHuyen.tinhthanh_id==tinh_thanh_id, QuanHuyen.active == "1").all()
        return {
            "msg":"Thành công",
            "results":schema.dump(query)
        }


class XaPhuongGetAll(Resource):
    @jwt_required()
    def get(self, ):
        schema = XaPhuongSchema(many=True)
        query = XaPhuong.query.filter(XaPhuong.active == "1").all()
        return {
            "msg":"Thành công",
            "results":schema.dump(query)
        }

class XaPhuongGetById(Resource):
    @jwt_required()
    def get(self, quan_huyen_id):
        schema = XaPhuongSchema(many=True)
        query = XaPhuong.query.filter(XaPhuong.quanhuyen_id == quan_huyen_id).all()
        return {
            "msg":"Thành công",
            "results":schema.dump(query)
        }