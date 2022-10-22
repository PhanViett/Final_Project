from application.controllers.in_ho_so.resources import InHoSo
from application.extensions import apispec
from flask import Blueprint, Flask, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.utils.resource.http_code import HttpCode

blueprint = Blueprint("in_ho_so", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(InHoSo, "/in_ho_so", endpoint="in_ho_so")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):

    return {
        'errorCode': "EC09",
        "msg": e.messages[next(iter(e.messages))][0]
    }, HttpCode.BadRequest
