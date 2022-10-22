from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.utils.resource.http_code import HttpCode
from application.controllers.duoc_si.bang_cap.resources import BangCapResource, BangCapById,BangCapGetList
from application.schemas import BangCapSchema
from flask import Flask

blueprint = Blueprint("bang_cap", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


api.add_resource(BangCapById, "/bang_cap/<id>", endpoint="bang_cap_by_id")
api.add_resource(BangCapResource, "/bang_cap", endpoint="bang_cap")
api.add_resource(BangCapGetList, "/bang_cap_get_list", endpoint="bang_cap_get_list")
# api.add_resource(BangCapDetails, "/bang_cap_get_details<id>", endpoint="bang_cap_get_details")


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
