from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.schemas.co_so_thuc_hanh import CoSoThucHanhSchema
from application.utils.resource.http_code import HttpCode
from application.controllers.duoc_si.co_so_thuc_hanh.resources import CoSoThucHanhResource,CoSoThucHanhById,CoSoThucHanhGetList
from flask import Flask

blueprint = Blueprint("co_so_thuc_hanh", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


api.add_resource(CoSoThucHanhResource, "/co_so_thuc_hanh_add", endpoint="co_so_thuc_hanh")
api.add_resource(CoSoThucHanhById, "/co_so_thuc_hanh_by_id/<id>", endpoint="co_so_thuc_hanh_by_id")
api.add_resource(CoSoThucHanhGetList, "/co_so_thuc_hanh_get_list", endpoint="co_so_thuc_hanh_get_list")




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
