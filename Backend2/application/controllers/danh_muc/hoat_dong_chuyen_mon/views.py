
from marshmallow import ValidationError
from application.controllers.danh_muc.hoat_dong_chuyen_mon.resources.hoat_dong_chuyen_mon import PhamViHoatDongChuyenMonResource,PhamViHoatDongChuyenMonGetList,PhamViHoatDongChuyenMonById
from application.extensions import apispec

from flask import Blueprint, current_app
from flask_restful import Api
from application.schemas.danhmuc_pham_vi_hoat_dong_chuyen_mon import PhamViHoatDongChuyenMonSchema
# from application.schemas.danhmuc_thanh_phan_ho_so import ThanhPhanHoSoSchema

# from application.schemas.danhmuc_noi_tot_nghiep import NoiTotNghiepSchema
from application.utils.resource.http_code import HttpCode

from flask import Flask




blueprint = Blueprint("pham_vi_hoat_dong_chuyen_mon",__name__,url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(PhamViHoatDongChuyenMonResource,"/danhmuc/pham_vi_hoat_dong_chuyen_mon_add", endpoint="Resource")
api.add_resource(PhamViHoatDongChuyenMonById,"/danhmuc/pham_vi_hoat_dong_chuyen_mon/<id>", endpoint="ById")
api.add_resource(PhamViHoatDongChuyenMonGetList,"/danhmuc/pham_vi_hoat_dong_chuyen_mon_get_list", endpoint="GetList")



     
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