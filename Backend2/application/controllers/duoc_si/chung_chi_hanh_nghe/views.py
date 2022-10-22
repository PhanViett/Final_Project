
from marshmallow import ValidationError

from application.controllers.duoc_si.chung_chi_hanh_nghe.resources.chung_chi_hanh_nghe import (
    ChungChiHanhNgheCompare, ChungChiHanhNgheCreate, ChungChiHanhNgheLienKetResource,
    ChungChiHanhNgheById, TimKiemTheoTen, ChungChiHanhNgheGetList,
    ChungChiHanhNgheGetInfo, ChungChiHanhNgheLuuThongTin, ChungChiHanhNgheGuiYeuCau,
    ChungChiHanhNgheTuChoiLienKetResource, ChungChiHanhNgheSearchSoGiayPhep, ChungChiHanhNgheGetCurrentInfo,
    CCHNDaCapGetList
)

from application.extensions import apispec

from flask import Blueprint, current_app
from flask_restful import Api

from application.schemas.chung_chi_hanh_nghe import ChungChiHanhNgheSchema
from application.utils.resource.http_code import HttpCode
from flask import Flask


blueprint = Blueprint("chung_chi_hanh_nghe", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(ChungChiHanhNgheCreate, "/duoc_si/chung_chi_hanh_nghe", endpoint="Resource")
api.add_resource(ChungChiHanhNgheById, "/duoc_si/chung_chi_hanh_nghe/<id>")
api.add_resource(ChungChiHanhNgheGetCurrentInfo, "/duoc_si/chung_chi_hanh_nghe")
api.add_resource(TimKiemTheoTen, "/duoc_si/chung_chi_hanh_nghe/<string:ten>")
api.add_resource(CCHNDaCapGetList, "/duoc_si/chung_chi_hanh_nghe_da_cap/get_list")

# api.add_resource(ChungChiHanhNgheById,"/duoc_si/chung_chi_hanh_nghe_by_id/<id>", endpoint="ById")

api.add_resource(TimKiemTheoTen, "/duoc_si/chung_chi_hanh_nghe_search", endpoint="Search_Name")

api.add_resource(ChungChiHanhNgheGetList, "/duoc_si/danh_sach_lien_ket/get_list")
api.add_resource(ChungChiHanhNgheCompare, "/duoc_si/danh_sach_lien_ket/<id>")
api.add_resource(ChungChiHanhNgheLienKetResource, "/duoc_si/duyet_lien_ket/<id>")
api.add_resource(ChungChiHanhNgheTuChoiLienKetResource, "/duoc_si/tu_choi_lien_ket/<id>")

api.add_resource(ChungChiHanhNgheGetInfo, "/duoc_si/info")
api.add_resource(ChungChiHanhNgheLuuThongTin, "/duoc_si/luu_chung_chi")
api.add_resource(ChungChiHanhNgheGuiYeuCau, "/duoc_si/yeu_cau_lien_ket")

api.add_resource(ChungChiHanhNgheSearchSoGiayPhep, "/duoc_si/search_so_giay_phep")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    return {
        "msg": "; ".join([key+" has "+", ".join(value) for key, value in e.messages.items()])
    }, HttpCode.BadRequest
