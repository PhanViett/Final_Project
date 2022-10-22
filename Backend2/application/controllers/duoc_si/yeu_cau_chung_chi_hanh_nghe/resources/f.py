import json
from marshmallow import ValidationError
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from application.commons.pagination import paginate
from application.controllers.duoc_si import chung_chi_hanh_nghe
from application.models.bang_cap import BangCap
from application.models.danhmuc_thu_tuc import DanhMucThuTuc
from application.models.danhmuc_vi_tri_hanh_nghe import ViTriHanhNghe
from application.models.lich_su_dao_tao import LichSuDaoTao
from application.models.user import User
from application.models.yeu_cau_chung_chi_hanh_nghe import YeuCauChungChiHanhNghe
from application.schemas import yeu_cau_chung_chi_hanh_nghe
from application.schemas.bang_cap import BangCapSchema
from application.schemas import nhan_vien
from application.schemas.danhmuc_vi_tri_hanh_nghe import ViTriHanhNgheSchema
from application.schemas.dao_tao import DaotaoSchema
from application.schemas.nhan_vien import NhanVienSchema
from application.schemas.yeu_cau_chung_chi_hanh_nghe import YeuCauChungChiHanhNgheGetListPaginateSchema, YeuCauChungChiHanhNgheSchema
from application.utils.helper.convert_timestamp_helper import current_milli_time, plus_time
from application.utils.helper.generate_so_thu_tu import generate_number
from application.utils.helper.string_processing_helper import clean_string
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
from application.utils.validate.uuid_validator import is_valid_uuid
from sqlalchemy import and_
from application.extensions import db


@jwt_required()
class ChungChiHanhNghePost(Resource):
    def get(self, id):

        user_schema = NhanVienSchema()
        dao_tao_schema = DaotaoSchema(many=True)
        bang_cap_schema = BangCapSchema(many=True)

        yeu_cau_chung_chi = YeuCauChungChiHanhNghe.query.filter(YeuCauChungChiHanhNghe.id == id).first()

        user = User.query.filter(User.id == current_user.id).first()

        dao_tao = LichSuDaoTao.query.filter(LichSuDaoTao.nhan_vien_id == user.id)

        bang_cap = BangCap.query.filter(BangCap.nhan_vien_id == user.id)

        if yeu_cau_chung_chi is None:
            return {"msg": "Don Yeu Cau Chứng Chỉ Không Tồn Tại"}, HttpCode.NotFound

        check_thutuc = DanhMucThuTuc.query.filter(DanhMucThuTuc.id == yeu_cau_chung_chi.thu_tuc_id).first()

        if check_thutuc.ma_thu_tuc == 'TT001':

            vi_hanh_nghe_schema = ViTriHanhNgheSchema(many=True)

            danh_muc_A = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'A')

            checked_danhmuc = []
            for danhmuc_A in ViTriHanhNgheSchema(many=True).dump(yeu_cau_chung_chi.vi_tri_hanh_nghe):
                checked_danhmuc.append(danhmuc_A.get("id"))
            danh_muc_B = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'B')
            danh_muc_C = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'C')
            danh_muc_D = ViTriHanhNghe.query.filter(ViTriHanhNghe.loai == 'D')

            loai_de_nghi = json.load(open('application/jsonFile/loai_cap_chung_chi.json', encoding='utf-8'))
            hinh_thuc_thi = json.load(open('application/jsonFile/hinh_thuc_thi.json', encoding='utf-8'))

            return {
                "result": {
                    "thu_tuc": {
                        "ten": check_thutuc.ten,
                        "loai": "1",
                    },
                    "user": user_schema.dump(user),
                    "dao_tao":  dao_tao_schema.dump(dao_tao),
                    "bang_cap": bang_cap_schema.dump(bang_cap),
                    "co_so_thuc_hanh": "Chua co api",
                    "de_nghi":
                        {
                            "loai_de_nghi": loai_de_nghi,
                            "hinh_thuc_thi": hinh_thuc_thi,
                            "danh_muc_pham_vi_hn": [
                                {
                                    "ten": "Chịu trách nhiệm chuyên môn về dược của",
                                    "value": vi_hanh_nghe_schema.dump(danh_muc_A),
                                },
                                {
                                    "ten": "Phụ trách về bảo đảm chất lượng",
                                    "value": vi_hanh_nghe_schema.dump(danh_muc_B),
                                },
                                {
                                    "ten": "Chịu trách nhiệm chuyên môn về dược, người phụ trách về bảo đảm chất lượng",
                                    "value": vi_hanh_nghe_schema.dump(danh_muc_C),
                                },
                                {
                                    "ten": "Phụ trách công tác dược lâm sàng",
                                    "value": vi_hanh_nghe_schema.dump(danh_muc_D),
                                },
                            ],
                            "checked_danh_muc_pham_vi_hn": [
                                {
                                    "value": checked_danhmuc,
                                }
                            ],
                    }
                }
            }, HttpCode.OK

        if check_thutuc.ma_thu_tuc == 'TT002':

            return {
                "result": {
                    "thu_tuc": {
                        "ten": check_thutuc.ten + "(Do thay đổi phạm vi hành nghề, hình thức cấp CCHND, hoặc thông tin của người hành nghề như Số chứng minh nhân dân, địa chỉ thường trú,…)",
                        "loai": "2",
                    },
                    "user": user_schema.dump(user),
                    "dao_tao":  dao_tao_schema.dump(dao_tao),
                    "bang_cap": bang_cap_schema.dump(bang_cap),
                    "lich_su_chung_chi": "Chua co api",
                }
            }, HttpCode.OK
        # return {"errors": "ERRORS"},  HttpCode.InternalError

        if check_thutuc.ma_thu_tuc == 'TT003':

            return {
                "result": {
                    "thu_tuc": {
                        "ten": check_thutuc.ten,
                        "loai": "3",
                    },
                    "user": user_schema.dump(user),
                    "dao_tao":  dao_tao_schema.dump(dao_tao),
                    "bang_cap": bang_cap_schema.dump(bang_cap),
                    "lich_su_chung_chi": "Chua co api",
                }
            }, HttpCode.OK
        return {"errors": "ERRORS"},  HttpCode.InternalError
