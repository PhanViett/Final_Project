from flask_restful import Api
from marshmallow import ValidationError
from flask import Blueprint, current_app, jsonify
from application.utils.resource.http_code import HttpCode
from application.controllers.tin_tuc.resources import TinTucGetList, TinTucGetListView, TinTucDetail, TinTucCreate, TinTucUpdate, TinTucDelete



blueprint = Blueprint("tin_tuc", __name__, url_prefix="/api/v1")
api = Api(blueprint)

@blueprint.before_app_first_request
def register_views():
    api.add_resource(TinTucGetList, "/tin-tuc-get-list", endpoint="tin-tuc-get-list")
    api.add_resource(TinTucGetListView, "/tin-tuc-get-list-view", endpoint="tin-tuc-get-list-view")
    api.add_resource(TinTucDetail, "/tin-tuc-detail", endpoint="tin-tuc-detail")
    api.add_resource(TinTucCreate, "/tin-tuc-create", endpoint="tin-tuc-create")
    api.add_resource(TinTucUpdate, "/tin-tuc-update/<id>", endpoint="tin-tuc-update")
    api.add_resource(TinTucDelete, "/tin-tuc-delete/<id>", endpoint="tin-tuc-delete")

@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    return {
        "msg": "; ".join([key+" has "+", ".join(value) for key, value in e.messages.items()])
    }, HttpCode.BadRequest
