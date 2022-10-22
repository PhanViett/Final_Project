from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.schemas.gps import GPSSchema
from application.utils.resource.http_code import HttpCode
from application.controllers.gps.resources import  GPSResource,GPSById,GPSGetList
from application.schemas import CoSoKinhDoanhSchema
from flask import Flask

blueprint = Blueprint("ma_loai", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


# api.add_resource(CoSoKinhDoanhById, "/co_so_kinh_doanh/<id>", endpoint="co_so_by_id")
api.add_resource(GPSResource, "/ma_loai_gps_add", endpoint="ma_loai_gps_add")
api.add_resource(GPSById, "/ma_loai_gps_by_id/<id>", endpoint="ma_loa_gps_by_id")
api.add_resource(GPSGetList, "/ma_loai__gps_get_list_gps", endpoint="ma_loai_get_list")


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
