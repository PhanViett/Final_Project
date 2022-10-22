from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.schemas.nhan_vien import QuanLyNguoiDungSchema
from application.utils.resource.http_code import HttpCode
from application.controllers.nhan_vien.quan_ly_nguoi_dung.resources.quan_ly_nguoi_dung import (
    QuanLyThongTinNguoiDungResource, QuanLyNguoiDungById,
    QuanLyNguoiDungGetList, QuanLyNguoiDungUpdateInfo, QuanLyNguoiDungCreateLanhDao
)
from flask import Flask

blueprint = Blueprint("quan_ly_nguoi_dung", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


api.add_resource(QuanLyNguoiDungById, "/quan_ly_nguoi_dung_by_id/<id>", endpoint="quan_ly_nguoi_dung_ById")
api.add_resource(QuanLyThongTinNguoiDungResource, "/quan_ly_nguoi_dung_add", endpoint="quan_ly_nguoi_dung_resource")
# api.add_resource(GPSById, "/ma_loai_gps_by_id/<id>", endpoint="ma_loa_gps_by_id")
api.add_resource(QuanLyNguoiDungGetList, "/quan_ly_nguoi_dung_get_list", endpoint="quan_ly_nguoi_dung_getlist")
api.add_resource(QuanLyNguoiDungUpdateInfo, "/quan_ly_nguoi_dung_update/<id>")
api.add_resource(QuanLyNguoiDungCreateLanhDao, "/quan_ly_nguoi_dung_create_lanh_dao")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    return {
        "msg": "; ".join([key+" has "+", ".join(value) for key, value in e.messages.items()])
    }, HttpCode.BadRequest
