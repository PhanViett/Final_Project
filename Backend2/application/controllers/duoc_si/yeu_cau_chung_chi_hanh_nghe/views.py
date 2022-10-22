from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.controllers.duoc_si.yeu_cau_chung_chi_hanh_nghe.resources.yeu_cau_chung_chi_hanh_nghe import TrangThaiHoSo, YeuCauChungChiUpdateThongTin
from application.extensions import apispec
from application.schemas.dao_tao import DaotaoSchema
from application.utils.resource.http_code import HttpCode
from application.controllers.duoc_si.yeu_cau_chung_chi_hanh_nghe.resources import ChungChiHanhNghePost,YeuCauChungChiHanhNgheById,YeuCauChungChiGetListById, YeuCauChungChiGetListAll, YeuCauChungChiGetDetailInList, YeuChungChiThuLy, PutCCHNDDuThao, ChangeMultiStatus, UpdateCCHNDChuyenVienHoiDong
from application.schemas import YeuCauChungChiHanhNgheSchema
from flask import Flask

blueprint = Blueprint("yeu_cau_chung_chi_hanh_nghe", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)


# api.add_resource(DaoTaoById, "/yeu_cau_chung_chi_hanh_nghe/<id>", endpoint="dao_tao_by_id")
api.add_resource(ChungChiHanhNghePost, "/yeu_cau_chung_chi_hanh_nghe", endpoint="yeu_cau_chung_chi_hanh_nghe")
api.add_resource(YeuCauChungChiHanhNgheById, "/yeu_cau_chung_chi_hanh_nghe/<id>", endpoint="yeu_cau_chung_chi_hanh_nghe_id")
api.add_resource(YeuCauChungChiGetListById, "/yeu_cau_chung_chi_hanh_nghe_getlist", endpoint="yeu_cau_chung_chi_hanh_nghe_getlist")
api.add_resource(YeuCauChungChiGetListAll, "/yeu_cau_chung_chi_hanh_nghe/get_all", endpoint="getAll")
api.add_resource(YeuCauChungChiGetDetailInList, "/yeu_cau_chung_chi_hanh_nghe/detail/<id>", endpoint="get_detail")
api.add_resource(YeuChungChiThuLy, "/yeu_cau_chung_chi_hanh_nghe/thu_ly", endpoint="thu_ly")
api.add_resource(TrangThaiHoSo, "/yeu_cau_chung_chi_hanh_nghe/trang_thai/<id>", endpoint="trang_thai")
api.add_resource(YeuCauChungChiUpdateThongTin, "/yeu_cau_chung_chi_hanh_nghe/update_inform/<id>", endpoint="inform")
api.add_resource(PutCCHNDDuThao, "/yeu_cau_chung_chi_hanh_nghe/update_du_thao/<id>", endpoint="update_du_thao")
api.add_resource(ChangeMultiStatus, "/yeu_cau_chung_chi_hanh_nghe/change_multi", endpoint="multi_hoso")
api.add_resource(UpdateCCHNDChuyenVienHoiDong, "/yeu_cau_chung_chi_hanh_nghe/trinh_hoi_dong/<id>", endpoint="trinh_hoi_dong")

@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return {
        'errorCode': "EC09",
        "msg": e.messages
    }, HttpCode.BadRequest
