
from marshmallow import ValidationError
from application.extensions import apispec

from flask import Blueprint, current_app
from flask_restful import Api

from application.controllers.vai_tro.resources.vai_tro import VaiTroResource, VaiTroById, VaiTroGetList, VaiTroSelectList


from application.schemas.danhmuc_loai_hình_kinh_doanh import LoaiHinhKinhDoanhSchema
from application.schemas.danhmuc_noi_tot_nghiep import NoiTotNghiepSchema
from application.schemas.vai_tro import VaiTroSchema
from application.utils.resource.http_code import HttpCode
from flask import Flask


blueprint = Blueprint("vai_tro", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(VaiTroResource, "/vai_tro", endpoint="Resource")
api.add_resource(VaiTroById, "/vai_tro/<id>", endpoint="ById")
api.add_resource(VaiTroGetList, "/vai_tro_get_list", endpoint="GetList")
api.add_resource(VaiTroSelectList, "/vai_tro_select_box")


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
