from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.controllers.co_so.giay_phep_kinh_doanh.resources.giay_phep_kinh_doanh import (
    GiayPhepKinhDoanhPost, GiayPhepKinhDoanhUpdateById, GiayPhepkinhDoanhGetList, CSKDGetYeuCauLienKet,
    GPKDGetDisplayInfo, GPKDLienKet, GPKDLuuThongTin, GPKDGuiDeNghiLienKet, GPKDCompare,
    GPKDDuyetLienKet, GPKDTuChoiLienKet
)
from application.extensions import apispec
from application.schemas.giay_phep_kinh_doanh import GiayPhepKinhDoanhSchema
from application.utils.resource.http_code import HttpCode
from flask import Flask

blueprint = Blueprint("giay_phep_kinh_doanh", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


api.add_resource(GiayPhepKinhDoanhUpdateById, "/co_so/giay_phep_kinh_doanh_by_id/<id>",
                 endpoint="giay_phep_kinh_doanh_by_id")
api.add_resource(GiayPhepKinhDoanhPost, "/co_so/giay_phep_kinh_doanh", endpoint="giay_phep_kinh_doanh")
api.add_resource(GiayPhepkinhDoanhGetList, "/co_so/giay_phep_kinh_doanh_get_list",
                 endpoint="giay_phep_kinh_doanh_get_list")
api.add_resource(CSKDGetYeuCauLienKet, "/co_so/giay_phep_kinh_doanh_lien_ket/get_list")
api.add_resource(GPKDGetDisplayInfo, "/co_so/giay_phep_kinh_doanh/info")
api.add_resource(GPKDLienKet, "/co_so/gpkd_lien_ket")
api.add_resource(GPKDLuuThongTin, "/co_so/gpkd_lien_ket/luu_giay_phep")
api.add_resource(GPKDGuiDeNghiLienKet, "/co_so/gpkd_lien_ket/yeu_cau_lien_ket")
api.add_resource(GPKDCompare, "/co_so/gpkd_lien_ket/<id>")
api.add_resource(GPKDDuyetLienKet, "/co_so/gpkd_lien_ket/duyet_lien_ket/<id>")
api.add_resource(GPKDTuChoiLienKet, "/co_so/gpkd_lien_ket/tu_choi_lien_ket/<id>")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    return {
        "msg": "; ".join([key+" has "+", ".join(value) for key, value in e.messages.items()])
    }, HttpCode.BadRequest
