
from marshmallow import ValidationError
from application.extensions import apispec

from flask import Blueprint, current_app
from flask_restful import Api

from application.controllers.thong_bao.resources.thong_bao import ThongBaoResource, ThongBaoGetList, ThongBaoDetails, ThongBaoRead
from application.schemas.bang_thong_bao import ThongBaoSchema


from application.schemas.danhmuc_loai_hình_kinh_doanh import LoaiHinhKinhDoanhSchema
from application.schemas.danhmuc_noi_tot_nghiep import NoiTotNghiepSchema
from application.schemas.vai_tro import VaiTroSchema
from application.utils.resource.http_code import HttpCode
from flask import Flask


blueprint = Blueprint("thong_bao", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(ThongBaoResource, "/thong_bao", endpoint="Resource")
api.add_resource(ThongBaoGetList, "/thong_bao", endpoint="GetList")
api.add_resource(ThongBaoDetails, "/thong_bao/<id>", endpoint="GetDetail")
api.add_resource(ThongBaoRead, "/thong_bao/read/<id>")


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
