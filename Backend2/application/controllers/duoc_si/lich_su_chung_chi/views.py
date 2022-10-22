from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.utils.resource.http_code import HttpCode
from application.controllers.duoc_si.lich_su_chung_chi.resources import LichSuChungChiResource,LichSuChungChiById,LichSuChungChiGetList
from application.schemas import LichSuChungChiSchema
from flask import Flask

blueprint = Blueprint("lich_su_chung_chi", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


api.add_resource(LichSuChungChiById, "/lich_su_chung_chi_by_id/<id>", endpoint="lich_su_chung_chi_by_id")
api.add_resource(LichSuChungChiResource, "/lich_su_chung_chi", endpoint="lich_su_chung_chi")
api.add_resource(LichSuChungChiGetList, "/lich_su_chung_chi_get_list", endpoint="lich_su_chung_chi_get_list")



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
