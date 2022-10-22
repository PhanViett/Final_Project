from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.schemas.loai_ma_chung_chi import LoaiMaChungChichema
from application.utils.resource.http_code import HttpCode
from application.controllers.loai_ma_chung_chi.resources import LoaiMaChungChiResource,LoaiMaChungChiById,LoaiMaChungChiGetList , FilterByDoiTuong, GetDetail
from flask import Flask

blueprint = Blueprint("ma_loai_chung_chi", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


api.add_resource(LoaiMaChungChiResource, "/ma_loai_chung_chi_add", endpoint="ma_loai_chung_chi_add")
api.add_resource(LoaiMaChungChiById, "/ma_loai_chung_chi_by_id/<id>", endpoint="ma_loai_id")
api.add_resource(LoaiMaChungChiGetList, "/ma_loai_chung_chi_get_list", endpoint="ma_loai_chung_chi_get_list")
api.add_resource(FilterByDoiTuong, "/loai_chung_chi/<doi_tuong_id>", endpoint="by_doi_tuong")
api.add_resource(GetDetail, "/loai_chung_chi_detail/<id>", endpoint="get_detail")




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
