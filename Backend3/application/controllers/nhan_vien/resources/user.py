from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from application.models.tai_khoan import TaiKhoan
from application.utils.resource.http_code import HttpCode
from application.models import Users
from application.commons.pagination import paginate
from application.utils.helper.string_processing_helper import clean_string
from application.schemas.nhan_vien import NguoiDungDisplaySchema


class QuanLyNguoiDungGetList(Resource):
    @ jwt_required()
    def post(self):
        schema = NguoiDungDisplaySchema(many=True)
        query = Users.query.filter(Users.active == True)
        data = request.json
        
        if not data:
            query = query.order_by(Users.ten_khong_dau.asc())
            return paginate(query, schema), HttpCode.OK

        elif data.get("search"):
            search_key = data["search"]
            query = query.filter(Users.ten_khong_dau.like(f"%{clean_string(search_key)}%"))

        query = query.order_by(Users.ten_khong_dau.asc())
        res = paginate(query, schema)

        if len(res["results"]) < 1:
        
            return {
                "msg": "Không có tên người dùng!!"
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
        
        