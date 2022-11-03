from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from application.models.record import Records
from application.commons.pagination import paginate
from application.schemas.record import RecordSchema
from application.utils.resource.http_code import HttpCode


class RecordGetList(Resource):
    @ jwt_required()
    def post(self):
        schema = RecordSchema(many=True)
        query = Records.query.filter()
        data = request.json
        
        if not data:
            query = query.order_by(Records.created_at.desc())
            return paginate(query, schema), HttpCode.OK

        elif data.get("id"):
            search_key = data["id"]
            query = query.filter(Records.user_id == search_key)

        query = query.order_by(Records.created_at.desc())
        res = paginate(query, schema)

        if len(res["results"]) < 1:
        
            return {
                "msg": "Người dùng này không có lịch sử chẩn đoán!!"
            }, HttpCode.OK

        return res, HttpCode.OK



# class QuanLyNguoiDungPost(Resource):
#     @ jwt_required()
#     def post(self):
#         data = request.json
        
#         exist_tai_khoan = TaiKhoan.query.filter(TaiKhoan.tai_khoan.like(data["tai_khoan"])).first()
#         if exist_tai_khoan:
#             return {
#                 "msg": "Tên đăng nhập đã tồn tại"
#             }, HttpCode.BadRequest
        
        