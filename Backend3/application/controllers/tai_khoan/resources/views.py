from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from application.models.tai_khoan import TaiKhoan
from application.commons.pagination import paginate
from application.schemas.tai_khoan import TaiKhoanSchema
from application.utils.resource.http_code import HttpCode


class TaiKhoanGetList(Resource):
    @ jwt_required()
    def post(self):
        schema = TaiKhoanSchema(many=True)
        query = TaiKhoanSchema.query.filter()
        data = request.json
        
        if not data:
            query = query.order_by(TaiKhoan.created_at.desc())
            return paginate(query, schema), HttpCode.OK

        elif data.get("id"):
            search_key = data["id"]
            query = query.filter(TaiKhoan.user_id == search_key)

        query = query.order_by(TaiKhoan.created_at.desc())
        res = paginate(query, schema)

        if len(res["results"]) < 1:
        
            return {
                "msg": "Người dùng này không có lịch sử chẩn đoán!!"
            }, HttpCode.OK

        return res, HttpCode.OK
