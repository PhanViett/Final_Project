from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.schemas.dao_tao import DaotaoSchema
from application.utils.resource.http_code import HttpCode
from application.controllers.duoc_si.dao_tao.resources import DaoTaoById,DaoTaoResource,DaoTaoGetList
from application.schemas import BangCapSchema
from flask import Flask

blueprint = Blueprint("dao_tao", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


api.add_resource(DaoTaoById, "/dao_tao_by_id/<id>", endpoint="dao_tao_by_id")
api.add_resource(DaoTaoResource, "/dao_tao", endpoint="dao_tao")
api.add_resource(DaoTaoGetList, "/dao_tao_get_list", endpoint="dao_tao_get_list")

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
