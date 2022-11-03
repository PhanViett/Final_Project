from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.utils.resource.http_code import HttpCode
from application.controllers.nhan_vien.resources import QuanLyNguoiDungGetList


blueprint = Blueprint("nhan_vien", __name__, url_prefix="/api/v1")
api = Api(blueprint)

@blueprint.before_app_first_request
def register_views():
    api.add_resource(QuanLyNguoiDungGetList, "/user-get-list", endpoint="user-get-list")



@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    return {
        "msg": "; ".join([key+" has "+", ".join(value) for key, value in e.messages.items()])
    }, HttpCode.BadRequest

