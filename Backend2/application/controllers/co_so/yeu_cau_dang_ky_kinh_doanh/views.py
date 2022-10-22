from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.schemas.yeu_cau_dang_ky_kinh_doanh import YeuCauDangKyKinhDoanhSchema
from application.utils.resource.http_code import HttpCode
from application.controllers.co_so.yeu_cau_dang_ky_kinh_doanh.resources import DangKyKinhDoanhPost
from flask import Flask


blueprint = Blueprint("yeu_cau_dang_ky_kinh_doanh", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


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
