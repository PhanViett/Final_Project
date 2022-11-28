from application.controllers.records.resources.views import RecordGetList, RecordCreate, RecordDelete, RecordPredict
from application.extensions import apispec
from application.utils.resource.http_code import HttpCode
from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

blueprint = Blueprint("records", __name__, url_prefix="/api/v1")
api = Api(blueprint)

@blueprint.before_app_first_request
def register_views():
    api.add_resource(RecordGetList, "/record-get-list", endpoint="record-get-list")
    api.add_resource(RecordCreate, "/record-create", endpoint="record-create")
    api.add_resource(RecordDelete, "/record-delete/<id>", endpoint="record-delete")
    api.add_resource(RecordPredict, "/record-predict", endpoint="record-predict")

@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    return {
        "msg": "; ".join([key+" has "+", ".join(value) for key, value in e.messages.items()])
    }, HttpCode.BadRequest

