from marshmallow import ValidationError
from application.extensions import apispec
from flask import Blueprint, current_app
from flask_restful import Api
from application.controllers.danh_sach_filter_condition.resources.danh_sach_filter_condition import ConditionDanhSachDuocSiFilter
from application.schemas.danhmuc_thu_tuc import DanhMucThuTucSchema
from application.utils.resource.http_code import HttpCode
from flask import Flask



blueprint = Blueprint("filter_danhsach",__name__,url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


api.add_resource(ConditionDanhSachDuocSiFilter,"/danh_sach/duoc_si", endpoint="duoc_si")

     
@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return {
        'errorCode': "EC09",
        "msg": e.messages[next(iter(e.messages))][0]
    }, HttpCode.BadRequest