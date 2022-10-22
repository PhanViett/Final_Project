
from marshmallow import ValidationError

from application.controllers.danh_muc.van_bang_chuyen_mon.resources.van_bang_chuyen_mon import VanBangChuyenMonResource, VanBangChuyenMonById, VanBangChuyenMonGetList,TimKiemTheoTen

from application.extensions import apispec

from flask import Blueprint, current_app
from flask_restful import Api

from application.schemas.danhmuc_van_bang_chuyen_mon import VanBangChuyenMonSchema
from application.utils.resource.http_code import HttpCode
from flask import Flask





blueprint = Blueprint("van_bang_chuyen_mon",__name__,url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(VanBangChuyenMonResource,"/danhmuc/van_bang_chuyen_mon_add", endpoint="Resource")
api.add_resource(VanBangChuyenMonById,"/danhmuc/van_bang_chuyen_mon/<id>", endpoint="ById")
api.add_resource(VanBangChuyenMonGetList,"/danhmuc/van_bang_chuyen_mon_get_list", endpoint="GetList")
api.add_resource(TimKiemTheoTen,"/danhmuc/van_bang_chuyen_mon_theo_ten", endpoint="GetTen")


     
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