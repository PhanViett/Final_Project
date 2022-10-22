
from datetime import datetime
from re import L
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError
from application.models.danhmuc_noi_tot_nghiep import NoiTotNghiep
from application.models.danhmuc_van_bang_chuyen_mon import VanBangChuyenMon
from application.models.duoc_si_co_so import DuocSiCoSo
from application.models.duoc_si_co_so_chua_giay_phep import DuocSiCoSoChuaGiayPhep
from application.models.lich_su_dao_tao import LichSuDaoTao
from application.models import CoSoKinhDoanh
from application.schemas.dao_tao import DaotaoSchema
from application.schemas.duoc_si_co_so import DuocSiCoSoSchema
from application.schemas.duoc_si_co_so_chua_giay_phep import DuocSiCoSoChuaGiayPhepSchema
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
from application.extensions import db
from application.commons.pagination import paginate


class DuocSiCoSoChuaGiayPhepResource(Resource):
    # add oke
    @jwt_required()
    def post(self):
        data = request.json
        schema = DuocSiCoSoChuaGiayPhepSchema()
        created_duoc_si = schema.load(data)

        db.session.add(created_duoc_si)
        db.session.commit()

        return {"msg": "Tạo thành công"}, HttpCode.Created


class DSCSCGPViaId(Resource):
    @jwt_required()
    def put(self, id):
        data = request.json
        schema = DuocSiCoSoChuaGiayPhepSchema(partial=True)
        duoc_si = DuocSiCoSoChuaGiayPhep.query.filter(DuocSiCoSoChuaGiayPhep.id == id).first()
        if duoc_si is None:
            return {"errors": "Không có thông tin nhập vào"},  HttpCode.InternalError
        dang_ky_kinh_doanh = schema.load(data, instance=duoc_si)
        db.session.commit()
        return {
            "msg": "Cập nhật thành công"
        }, HttpCode.OK

    @jwt_required()
    def delete(self, id):
        duoc_si = DuocSiCoSoChuaGiayPhep.query.filter(DuocSiCoSoChuaGiayPhep.id == id).first()
        db.session.delete(duoc_si)
        db.session.commit()
        return {
            "msg": "Xóa nhân viên hành nghề thành công"
        }, HttpCode.OK


class DuocSiCoSoChuaCogiayPhepGetList(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        query = DuocSiCoSoChuaGiayPhep.query

        if data.get("detail_id"):
            schema = DuocSiCoSoChuaGiayPhepSchema()
            duoc_si = query.filter(DuocSiCoSoChuaGiayPhep.id == data["detail_id"]).first()
            if not duoc_si:
                return {
                    "msg": "Dược sĩ không tồn tại"
                }, HttpCode.BadRequest
            return {
                "msg": "Thành công",
                "results": schema.dump(duoc_si)
            }, HttpCode.OK
        if not data.get("co_so_kinh_doanh_id"):
            return {
                "msg": "Thiếu co_so_kinh_doanh_id"
            }, HttpCode.BadRequest

        schema = DuocSiCoSoChuaGiayPhepSchema(many=True)
        query = query.order_by(DuocSiCoSoChuaGiayPhep.created_at.asc())
        return paginate(query, schema), HttpCode.OK


class DSCSCGPGetListCurrent(Resource):
    @jwt_required()
    def get(self):
        query = DuocSiCoSoChuaGiayPhep.query
        if not isinstance(current_user, CoSoKinhDoanh):
            return {
                "msg": "Người dùng không phải là một cơ sở kinh doanh"
            }, HttpCode.BadRequest
        current_co_so: CoSoKinhDoanh = current_user
        schema = DuocSiCoSoChuaGiayPhepSchema(
            many=True,
            only=["ho_ten", "ngay_sinh", "so_dien_thoai", "gioi_tinh", "bang_cap"]
        )
        query = query.filter(DuocSiCoSoChuaGiayPhep.co_so_kinh_doanh_id == current_co_so.id)
        query = query.order_by(DuocSiCoSoChuaGiayPhep.created_at.asc())
        return paginate(query, schema), HttpCode.OK
