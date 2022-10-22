
from marshmallow import ValidationError
from application.extensions import apispec

from flask import Blueprint, current_app
from flask_restful import Api

from application.controllers.danh_muc.hoi_dong.resources.hoi_dong import HoiDongResource,HoiDongById,HoiDongGetList
from application.schemas.danhmuc_hoi_dong import HoiDongSchema

from application.utils.resource.http_code import HttpCode
from flask import Flask


blueprint = Blueprint("hoi_dong",__name__,url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(HoiDongResource,"/danhmuc/hoidong_add", endpoint="Resource")
api.add_resource(HoiDongById,"/danhmuc/hoidong/<id>", endpoint="ById")
api.add_resource(HoiDongGetList,"/danhmuc/hoidong_get_list", endpoint="GetList")

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