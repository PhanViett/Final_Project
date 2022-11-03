from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.controllers.records.resources.views import RecordGetList
from application.extensions import apispec
from application.utils.resource.http_code import HttpCode


blueprint = Blueprint("records", __name__, url_prefix="/api/v1")
api = Api(blueprint)

@blueprint.before_app_first_request
def register_views():
    api.add_resource(RecordGetList, "/record-get-list", endpoint="record-get-list")



@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    return {
        "msg": "; ".join([key+" has "+", ".join(value) for key, value in e.messages.items()])
    }, HttpCode.BadRequest

