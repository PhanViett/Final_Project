from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.utils.resource.http_code import HttpCode
from application.controllers.co_so_kinh_doanh.resources import CoSoKinhDoanhResource, CoSoKinhDoanhById, CoSoKinhDoanhGetList
from application.schemas import CoSoKinhDoanhSchema
from flask import Flask

blueprint = Blueprint("co_so_kinh_doanh", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(CoSoKinhDoanhGetList, "/co_so_kinh_doanh/get_list", endpoint="co_so_get_list")
api.add_resource(CoSoKinhDoanhById, "/co_so_kinh_doanh/<id>", endpoint="co_so_by_id")
api.add_resource(CoSoKinhDoanhResource, "/co_so_kinh_doanh", endpoint="co_so")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    return {
        "msg": "; ".join([key+" has "+", ".join(value) for key, value in e.messages.items()])
    }, HttpCode.BadRequest
