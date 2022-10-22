from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.controllers.to_chuc.noi_dung_thuc_hanh.resources.noi_dung_thuc_hanh import NoiDungThucHanhResource,NoiDungThucHanhById,NoiDungThucHanhGetList

from application.extensions import apispec
from application.schemas.co_so_thuc_hanh import CoSoThucHanhSchema
from application.schemas.noi_dung_thuc_hanh import NoiDungThucHanhSchema
from application.utils.resource.http_code import HttpCode
from flask import Flask

blueprint = Blueprint("noi_dung_thuc_hanh", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


api.add_resource(NoiDungThucHanhResource, "/noi_dung_thuc_hanh_add", endpoint="noi_dung_thuc_hanh_add")
api.add_resource(NoiDungThucHanhById, "/noi_dung_thuc_hanh_by_id/<id>", endpoint="noi_dung_thuc_hanh_by_id")
api.add_resource(NoiDungThucHanhGetList, "/noi_dung_thuc_hanh_get_list", endpoint="noi_dung_thuc_hanh_get_list")


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
