
from marshmallow import ValidationError
from application.controllers.danh_muc.noi_tot_nghiep.resources.noi_tot_nghiep import NoiTotNghiepById, NoiTotNghiepGetList, NoiTotNghiepResource
from application.extensions import apispec

from flask import Blueprint, current_app
from flask_restful import Api

from application.schemas.danhmuc_noi_tot_nghiep import NoiTotNghiepSchema
from application.utils.resource.http_code import HttpCode

from flask import Flask




blueprint = Blueprint("noi_tot_nghiep",__name__,url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(NoiTotNghiepResource,"/danhmuc/noi_tot_nghiep_add", endpoint="Resource")
api.add_resource(NoiTotNghiepById,"/danhmuc/noi_tot_nghiep/<id>", endpoint="ById")
api.add_resource(NoiTotNghiepGetList,"/danhmuc/noi_tot_nghiep_get_list", endpoint="GetList")


     
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