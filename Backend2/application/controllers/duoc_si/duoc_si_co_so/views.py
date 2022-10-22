from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.schemas.dao_tao import DaotaoSchema
from application.schemas.duoc_si_co_so import DuocSiCoSoSchema
from application.utils.resource.http_code import HttpCode
from application.controllers.duoc_si.duoc_si_co_so.resources import DuocSiCoSoResource, DuocSiCoSoById, DuocSiCoSoGetList, DuocSiCoSoSetVaiTro
from application.schemas import BangCapSchema
from flask import Flask

blueprint = Blueprint("duoc_si_co_so", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


api.add_resource(DuocSiCoSoById, "/duoc_si_co_so/<id>")
api.add_resource(DuocSiCoSoResource, "/duoc_si_co_so")
api.add_resource(DuocSiCoSoGetList, "/duoc_si_co_so")
api.add_resource(DuocSiCoSoSetVaiTro, "/duoc_si_co_so/set_vai_tro")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):

    return {
        "msg": "; ".join([key+" has "+", ".join(value) for key, value in e.messages.items()])
    }, HttpCode.BadRequest
