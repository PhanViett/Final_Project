from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.utils.resource.http_code import HttpCode
from .resource.import_danhmuc_chung_chi import ImportUserResource
from flask import Flask

blueprint = Blueprint("chung_chi_import", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(ImportUserResource, "/chung_chi/import")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return {
        'errorCode': "EC09",
        "msg": e.messages
    }, HttpCode.BadRequest
