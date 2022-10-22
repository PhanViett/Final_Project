from marshmallow import ValidationError
from application.extensions import apispec

from flask import Blueprint, current_app
from flask_restful import Api
from application.schemas.quan_huyen import QuanHuyenSchema
from application.schemas.tinh_thanh import TinhThanhSchema
from .resources import (
    TinhThanhCreate, TinhThanhGetAll, TinhThanhGetPaginate, TinhThanhUpdateDelete,
    QuanHuyenCreate, QuanHuyenGetAll, QuanHuyenGetPaginate, QuanHuyenUpdateDelete,
    XaPhuongUpdateDelete, XaPhuongCreate, XaPhuongGetAll, XaPhuongGetPaginate)

# from application.schemas.danhmuc_noi_tot_nghiep import NoiTotNghiepSchema
from application.utils.resource.http_code import HttpCode
from flask import Flask

blueprint = Blueprint("location", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(TinhThanhGetAll, "/danhmuc/location/tinh-thanh/get-all")
api.add_resource(TinhThanhGetPaginate, "/danhmuc/location/tinh-thanh/get-paginate")
api.add_resource(TinhThanhCreate, "/danhmuc/location/tinh-thanh")
api.add_resource(TinhThanhUpdateDelete, "/danhmuc/location/CA-tinh-thanh")


api.add_resource(QuanHuyenGetAll, "/danhmuc/location/quan-huyen/get-all/<tinh_thanh_id>")
api.add_resource(QuanHuyenGetPaginate, "/danhmuc/location/quan-huyen/get-paginate")
api.add_resource(QuanHuyenCreate, "/danhmuc/location/quan-huyen")
api.add_resource(QuanHuyenUpdateDelete, "/danhmuc/location/quan-huyen")

api.add_resource(XaPhuongGetAll, "/danhmuc/location/xa-phuong/get-all/<quan_huyen_id>")
api.add_resource(XaPhuongGetPaginate, "/danhmuc/location/xa-phuong/get-paginate")
api.add_resource(XaPhuongCreate, "/danhmuc/location/xa-phuong")
api.add_resource(XaPhuongUpdateDelete, "/danhmuc/location/xa-phuong")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    return {
        "msg": "; ".join([key+" has "+", ".join(value) for key, value in e.messages.items()])
    }, HttpCode.BadRequest
