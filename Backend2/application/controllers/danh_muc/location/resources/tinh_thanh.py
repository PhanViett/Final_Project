from flask_restful import Resource
from application.models import TinhThanh
from application.schemas.tinh_thanh import TinhThanhDisplayCMNDSchema, TinhThanhSchema
from application.utils.validate.uuid_validator import is_valid_uuid
from application.extensions import db
from application.commons.pagination import paginate
from flask import request
from flask_jwt_extended import jwt_required


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


class TinhThanhUpdateDelete(Resource):
    @jwt_required()
    def put(self, id):
        data = request.json
        schema = TinhThanhSchema(partial=True)
        if not is_valid_uuid(id):
            return {
                "errorCode": "EC05",
                "msg": "ID sai định dạng (không phải UUID)"
            }
        target_tinh_thanh = TinhThanh.query.get_or_404(id)
        schema.load(data=data, instance=target_tinh_thanh)
        db.session.commit()
        return {
            "msg": "Thành công",
            "results": schema.dump(target_tinh_thanh)
        }

    @jwt_required()
    def delete(self, id):
        if not is_valid_uuid(id):
            return {
                "errorCode": "EC05",
                "msg": "ID sai định dạng (không phải UUID)"
            }
        target_tinh_thanh = TinhThanh.query.get_or_404(id)
        db.session.delete(target_tinh_thanh)
        db.session.commit()
        return {
            "msg": "Xóa tỉnh thành thành công"
        }

    @jwt_required()
    def get(self):
        schema = TinhThanhDisplayCMNDSchema(many=True)
        tinh_thanh_all = TinhThanh.query.all()

        return {
            "msg": "Thành công",
            "results": schema.dump(tinh_thanh_all)
        }


class TinhThanhGetPaginate(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        schema = TinhThanhSchema()
        if request.args.get("detail_id", None):
            detail_id = request.args.get["detail_id"]
            target_tinh_thanh = TinhThanh.query.get_or_404(detail_id)
            return {
                "msg": "Thành công",
                "results": schema.dump(target_tinh_thanh)
            }
        schema = TinhThanhSchema(many=True)
        query = TinhThanh.query.filter(TinhThanh.loai == 0)
        return paginate(query=query, schema=schema)


class TinhThanhCreate(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        schema = TinhThanhSchema()
        if "ten" not in data or not data["ten"]:
            return {
                "erroCode": "EC19",
                "msg": "Thiếu tên tỉnh thành"
            }
        exist = TinhThanh.query.filter(TinhThanh.ten.like(data["ten"])).first()
        if exist:
            return {
                "erroCode": "EC18",
                "msg": "tỉnh thành đã tồn tại"
            }
        created_quoc_gia = schema.load(data)
        db.session.add(created_quoc_gia)
        db.session.commit()
        return {
            "msg": "Thành công",
            "resultrs": schema.dump(created_quoc_gia)
        }
