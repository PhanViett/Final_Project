from flask_restful import Resource
from application.models import XaPhuong
from application.schemas.xa_phuong import XaPhuongSchema
from application.utils.validate.uuid_validator import is_valid_uuid
from application.extensions import db
from application.commons.pagination import paginate
from flask import request
from flask_jwt_extended import jwt_required

class XaPhuongGetAll(Resource):
    @jwt_required()
    def get(self, quan_huyen_id):
        schema = XaPhuongSchema(many=True)
        query = XaPhuong.query.filter(XaPhuong.quanhuyen_id == quan_huyen_id).all()
        return {
            "msg":"Thành công",
            "results":schema.dump(query)
        }
class XaPhuongUpdateDelete(Resource):
    @jwt_required()
    def put(self,id):
        data = request.json
        schema = XaPhuongSchema(partial=True)
        if not is_valid_uuid(id):
            return {
                "errorCode":"EC05",
                "msg":"ID sai định dạng (không phải UUID)"
            }
        target_quan_huyen = XaPhuong.query.get_or_404(id)
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
        target_quan_huyen = XaPhuong.query.get_or_404(id)
        db.session.delete(target_quan_huyen)
        db.session.commit()
        return {
            "msg":"Xóa tỉnh thành thành công"
        }

class XaPhuongGetPaginate(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        schema= XaPhuongSchema()
        if request.args.get("detail_id",None):
            detail_id = request.args.get["detail_id"]
            target_quan_huyen = XaPhuong.query.get_or_404(detail_id)
            return {
                "msg":"Thành công",
                "results": schema.dump(target_quan_huyen)
            }
        schema = XaPhuongSchema(many=True)
        query = XaPhuong.query
        return paginate(query=query, schema=schema)

class XaPhuongCreate(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        schema = XaPhuongSchema()
        if "ten" not in data or not data["ten"]:
            return {
                "erroCode":"EC19",
                "msg": "Thiếu tên tỉnh thành"
            }
        exist = XaPhuong.query.filter(XaPhuong.ten.like(data["ten"])).first()
        if exist:
            return {
                "erroCode":"EC18",
                "msg": "tỉnh thành đã tồn tại"
            }
        created_quoc_gia = schema.load(data)
        db.session.add(created_quoc_gia)
        db.session.commit()
        return {
            "msg":"Thành công",
            "resultrs": schema.dump(created_quoc_gia)
        }
