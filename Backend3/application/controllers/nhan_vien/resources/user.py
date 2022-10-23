from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from application.utils.resource.http_code import HttpCode
from application.models import Users
from application.commons.pagination import paginate
from application.utils.helper.string_processing_helper import clean_string
from application.schemas.nhan_vien import NguoiDungDisplaySchema


class QuanLyNguoiDungGetList(Resource):
    # @ jwt_required()
    def get(self):
        schema = NguoiDungDisplaySchema(many=True)
        query = Users.query.filter(Users.active == True)
        res = paginate(query, schema)
        if len(res["results"]) < 1:
            return {
                "msg": "Không có tên người dùng!!"
            }, HttpCode.OK

        return res, HttpCode.OK

    # @ jwt_required()
    def post(self):
        schema = NguoiDungDisplaySchema(many=True)
        query = Users.query.filter(Users.active == True)
        res = paginate(query, schema)
        if len(res["results"]) < 1:
            return {
                "msg": "Không có tên người dùng!!"
            }, HttpCode.OK

        return res, HttpCode.OK