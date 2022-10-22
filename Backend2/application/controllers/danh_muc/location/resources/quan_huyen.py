from flask_restful import Resource
from application.models import QuanHuyen
from application.schemas.quan_huyen import QuanHuyenSchema
from application.utils.validate.uuid_validator import is_valid_uuid
from application.extensions import db
from application.commons.pagination import paginate
from flask import request
from flask_jwt_extended import jwt_required

class QuanHuyenGetAll(Resource):
    @jwt_required()
    def get(self, tinh_thanh_id):
        schema = QuanHuyenSchema(many=True)
        query = QuanHuyen.query.filter(QuanHuyen.tinhthanh_id==tinh_thanh_id, QuanHuyen.active == "1").all()
        return {
            "msg":"Thành công",
            "results":schema.dump(query)
        }
class QuanHuyenUpdateDelete(Resource):
    @jwt_required()
    def put(self,id):
        data = request.json
        schema = QuanHuyenSchema(partial=True)
        if not is_valid_uuid(id):
            return {
                "errorCode":"EC05",
                "msg":"ID sai định dạng (không phải UUID)"
            }
        target_quan_huyen = QuanHuyen.query.get_or_404(id)
        schema.load(data=data, instance=target_quan_huyen)
        db.session.commit()
        return {
            "msg":"Thành công",
            "results": schema.dump(target_quan_huyen)
        }
    @jwt_required()
    def delete(self,id):
        if not is_valid_uuid(id):
            return {
                "errorCode":"EC05",
                "msg":"ID sai định dạng (không phải UUID)"
            }
        target_quan_huyen = QuanHuyen.query.get_or_404(id)
        db.session.delete(target_quan_huyen)
        db.session.commit()
        return {
            "msg":"Xóa quốc gia thành công"
        }

class QuanHuyenGetPaginate(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        schema= QuanHuyenSchema()
        if request.args.get("detail_id",None):
            detail_id = request.args.get["detail_id"]
            target_quan_huyen = QuanHuyen.query.get_or_404(detail_id)
            return {
                "msg":"Thành công",
                "results": schema.dump(target_quan_huyen)
            }
        schema = QuanHuyenSchema(many=True)
        query = QuanHuyen.query
        return paginate(query=query, schema=schema)

class QuanHuyenCreate(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        schema = QuanHuyenSchema()
        if "ten" not in data or not data["ten"]:
            return {
                "erroCode":"EC19",
                "msg": "Thiếu tên quốc gia"
            }
        exist = QuanHuyen.query.filter(QuanHuyen.ten.like(data["ten"])).first()
        if exist:
            return {
                "erroCode":"EC18",
                "msg": "Quốc gia đã tồn tại"
            }
        created_quoc_gia = schema.load(data)
        db.session.add(created_quoc_gia)
        db.session.commit()
        return {
            "msg":"Thành công",
            "resultrs": schema.dump(created_quoc_gia)
        }
