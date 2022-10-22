
from marshmallow import ValidationError
from application.controllers.danh_muc.quan_huyen_location.resources.quan_huyen import QuanHuyenById,GetQuanHuyen,GetQuanHuyenByTinhThanhID

from application.extensions import apispec

from flask import Blueprint, current_app
from flask_restful import Api
from application.schemas.quan_huyen import QuanHuyenSchema
from application.schemas.tinh_thanh import TinhThanhSchema

from application.utils.resource.http_code import HttpCode





blueprint = Blueprint("quan_huyen_location",__name__,url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(GetQuanHuyen,"/danhmuc/quan_huyen_location", endpoint="Resource")
api.add_resource(QuanHuyenById,"/danhmuc/quan_huyen_location/<id>", endpoint="ById")
api.add_resource(GetQuanHuyenByTinhThanhID,"/danhmuc/quan_huyen_location_by_tinh_thanh/<id>")



     
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