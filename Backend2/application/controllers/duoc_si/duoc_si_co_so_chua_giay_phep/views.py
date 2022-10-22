from flask import Blueprint
from flask_restful import Api
from marshmallow import ValidationError
from application.controllers.duoc_si.duoc_si_co_so_chua_giay_phep.resources.duoc_si_co_so_chua_giay_phep import (
    DuocSiCoSoChuaGiayPhepResource, DuocSiCoSoChuaCogiayPhepGetList, DSCSCGPViaId,
    DSCSCGPGetListCurrent
)
from application.utils.resource.http_code import HttpCode
# from application.controllers.duoc_si.duoc_si_co_so.resources import DuocSiCoSoResource,DuocSiCoSoById
from flask import Flask

blueprint = Blueprint("duoc_si_chua_giay_phep", __name__, url_prefix="/api/v2")
api = Api(blueprint, errors=Flask.errorhandler)

api.add_resource(DuocSiCoSoChuaCogiayPhepGetList, "/duoc_si_chua_giay_phep/get_list")
api.add_resource(DuocSiCoSoChuaGiayPhepResource, "/duoc_si_chua_giay_phep")
api.add_resource(DSCSCGPViaId, "/duoc_si_chua_giay_phep/<id>")
api.add_resource(DSCSCGPGetListCurrent, "/duoc_si_chua_giay_phep")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    return {
        "msg": "; ".join([key+" has "+", ".join(value) for key, value in e.messages.items()])
    }, HttpCode.BadRequest
