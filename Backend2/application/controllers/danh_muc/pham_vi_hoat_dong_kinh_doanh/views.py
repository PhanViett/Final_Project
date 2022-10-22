
from marshmallow import ValidationError
from application.controllers.danh_muc.pham_vi_hoat_dong_kinh_doanh.resources.pham_vi_hoat_dong_kinh_doanh import PhamViHoatDongKinhDoanhResource, PhamViHoatDongKinhDoanhById, PhamViHoatDongKinhDoanhGetList
from application.extensions import apispec

from flask import Blueprint, current_app
from flask_restful import Api
from application.schemas.danhmuc_pham_vi_hoat_dong_kinh_doanh import PhamVihoatDongKinhDoanhSchema
# from application.schemas.danhmuc_thanh_phan_ho_so import ThanhPhanHoSoSchema

# from application.schemas.danhmuc_noi_tot_nghiep import NoiTotNghiepSchema
from application.utils.resource.http_code import HttpCode
from flask import Flask





blueprint = Blueprint("pham_vi_hoat_dong_kinh_doanh",__name__,url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(PhamViHoatDongKinhDoanhResource,"/danhmuc/pham_vi_hoat_dong_kinh_doanh_add", endpoint="Resource")
api.add_resource(PhamViHoatDongKinhDoanhById,"/danhmuc/pham_vi_hoat_dong_kinh_doanh/<id>", endpoint="ById")
api.add_resource(PhamViHoatDongKinhDoanhGetList,"/danhmuc/pham_vi_hoat_dong_kinh_doanh_get_list", endpoint="GetList")

     
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