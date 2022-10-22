from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.schemas.chung_nhan_thuc_hanh_co_so import ChungNhanCoSoSchema
from application.utils.resource.http_code import HttpCode
from application.controllers.danh_muc.chung_nhan_thuc_hanh_co_so.resources import ThucHanhCoSoResource,ChungNhanCoSoById,ThucHanhCoSoGetList
from flask import Flask

blueprint = Blueprint("chung_nhan_thuc_hanh_co_so", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(ThucHanhCoSoResource, "/chung_nhan_thuc_hanh_co_so_add", endpoint="chung_nhan")
api.add_resource(ChungNhanCoSoById, "/chung_nhan_thuc_hanh_co_so_update/<id>", endpoint="co_so_by_id")
api.add_resource(ThucHanhCoSoGetList, "/chung_nhan_thuc_hanh_co_so_get_list", endpoint="GetList")



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
