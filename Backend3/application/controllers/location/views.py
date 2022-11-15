from application.extensions import apispec
from application.utils.resource.http_code import HttpCode
from flask import Blueprint, Flask, current_app
from flask_restful import Api
from marshmallow import ValidationError

from .resources import TinhThanhGetAll, QuanHuyenGetAll, QuanHuyenGetById, XaPhuongGetAll, XaPhuongGetById

blueprint = Blueprint("location", __name__, url_prefix="/api/v1")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(TinhThanhGetAll, "/danh-muc/tinh-thanh")
api.add_resource(QuanHuyenGetAll, "/danh-muc/quan-huyen")
api.add_resource(QuanHuyenGetById, "/danh-muc/quan-huyen/get-all/<tinh_thanh_id>")
api.add_resource(XaPhuongGetAll, "/danh-muc/xa-phuong")
api.add_resource(XaPhuongGetById, "/danh-muc/xa-phuong/get-all/<quan_huyen_id>")



@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    return {
        "msg": "; ".join([key+" has "+", ".join(value) for key, value in e.messages.items()])
    }, HttpCode.BadRequest
