from marshmallow import ValidationError
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from application.models.danhmuc_thu_tuc import DanhMucThuTuc
import json

from application.schemas.danhmuc_thu_tuc import DanhMucThuTucSchema
from application.utils.resource.http_code import HttpCode


class ConditionDanhSachDuocSiFilter(Resource):
    @jwt_required()
    def get(self):

        thu_tucs = []
        thu_tuc_query = DanhMucThuTuc.query.filter(DanhMucThuTuc.doi_tuong == '1').all()
        for thu_tuc in thu_tuc_query:
            thu_tucs.append(
                {
                    "label": thu_tuc.ten,
                    "value": str(thu_tuc.id),
                }
            )

        trang_thais = []
        with open('application/jsonFile/trang_thai_ho_so.json', encoding="UTF-8") as json_file:
            resp = json.load(json_file)
        for key, value in resp.items():
            trang_thais.append(
                {
                    "label": value,
                    "value": key
                }
            )

        het_hans = []
        with open('application/jsonFile/trang_thai_het_han.json', encoding="UTF-8") as json_files:
            response = json.load(json_files)
        for key, value in response.items():
            het_hans.append(
                {
                    "label": value,
                    "value": key
                }
            )
        return {
            "results": {
                "thu_tuc": thu_tucs,
                "trang_thai_ho_so": trang_thais,
                "het_hans": het_hans
            }
        }, HttpCode.OK
