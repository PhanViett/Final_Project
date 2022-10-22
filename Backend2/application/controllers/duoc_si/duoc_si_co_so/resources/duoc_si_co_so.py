
from re import L
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from application.models.chung_chi_hanh_nghe import ChungChiHanhNghe
from application.models.chung_nhan_thuc_hanh_co_so import ChungNhanCoSo
from application.models.co_so_kinh_doanh import CoSoKinhDoanh
from application.models.duoc_si_co_so import DuocSiCoSo
from application.models.user import User
from application.schemas.duoc_si_co_so import DuocSiCoSoDisplaySchema, DuocSiCoSoSchema
from application.utils.resource.http_code import HttpCode
from application.extensions import db
from application.commons.pagination import paginate
from application.utils.helper.string_processing_helper import clean_string
from sqlalchemy.orm import joinedload
from application.utils.validate.uuid_validator import is_valid_uuid


class DuocSiCoSoResource(Resource):
    @jwt_required()
    def post(self):
        schema = DuocSiCoSoSchema()
        req = {
            "chung_chi_id": request.form.get("chung_chi_id"),
            "co_so_kinh_doanh_id": request.form.get("co_so_kinh_doanh_id"),
            "vai_tro": request.form.get("vai_tro")
        }

        duoc_Si = schema.load(req)
        # duoc_Si.vaitro = current_user.id
        db.session.add(duoc_Si)
        db.session.commit()
        return {"msg": "Tạo thành công", "results": schema.dump(duoc_Si)}, HttpCode.Created


class DuocSiCoSoById(Resource):
    @jwt_required()
    def put(self, id):
        schema = DuocSiCoSoSchema(partial=True)
        duoc_si = DuocSiCoSo.query.filter(DuocSiCoSo.id == id).first()
        if duoc_si is None:
            return {"errors": "No data"},  HttpCode.InternalError

        req = {
            "chung_chi_id": request.form.get("chung_chi_id"),
            "co_so_kinh_doanh_id": request.form.get("co_so_kinh_doanh_id"),
            "vai_tro": request.form.get("vai_tro")
        }
        duoc_si = schema.load(req, instance=duoc_si)
        db.session.commit()
        return {"msg": "Cập nhật thành công", "results": schema.dump(duoc_si)}, HttpCode.OK

    @jwt_required()
    def delete(self, id):
        schema = DuocSiCoSoSchema()
        duoc_si_co_so = DuocSiCoSo.query.filter(DuocSiCoSo.id == id).first()
        if duoc_si_co_so is None:
            return {"errors": "Không có dữ liệu!"},  HttpCode.InternalError
        db.session.delete(duoc_si_co_so)
        db.session.commit()

        return {"msg": "xóa thành công!"}, HttpCode.OK


class DuocSiCoSoGetList(Resource):
    @jwt_required()
    def get(self):
        if not isinstance(current_user, CoSoKinhDoanh):
            return {
                "msg": "Người dùng không phải là một cơ sở kinh doanh"
            }, HttpCode.BadRequest
        current_co_so: CoSoKinhDoanh = current_user
        schema = DuocSiCoSoDisplaySchema(many=True)
        query = db.session.query(
            DuocSiCoSo.id,
            DuocSiCoSo.vai_tro,
            User.ho_ten,
            User.ngay_sinh,
            User.dien_thoai,
            ChungChiHanhNghe.so_giay_phep,
            ChungChiHanhNghe.ngay_hieu_luc.label("hieu_luc_den"))\
            .join(User, User.id == DuocSiCoSo.duoc_si_id)\
            .join(ChungChiHanhNghe, ChungChiHanhNghe.nhan_vien_id == User.id)\
            .filter(DuocSiCoSo.co_so_kinh_doanh_id == current_co_so.id)\
            .order_by(DuocSiCoSo.vai_tro, DuocSiCoSo.updated_at)
        return paginate(query, schema), HttpCode.OK


class DuocSiCoSoSetVaiTro(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        if not isinstance(current_user, CoSoKinhDoanh):
            return {
                "msg": "Người dùng không phải là một cơ sở kinh doanh"
            }, HttpCode.BadRequest
        current_co_so: CoSoKinhDoanh = current_user
        if not data.get("duoc_si_id"):
            return {
                "msg": "Thiếu dữ liệu nhân viên id"
            }, HttpCode.BadRequest
        if not is_valid_uuid(data.get("duoc_si_id")):
            return {
                "msg": "Id nhập vào không hợp lệ"
            }
        target_nhan_vien: User = User.query.options(joinedload(User.duoc_si_co_so).options(
                                                    joinedload(DuocSiCoSo.co_so_kinh_doanh))
                                                    ).get(data.get("duoc_si_id"))
        if not target_nhan_vien:
            return {
                "msg": "Nhân viên không tồn tại"
            }, HttpCode.NotFound

        duoc_si_co_so: DuocSiCoSo = target_nhan_vien.duoc_si_co_so
        if duoc_si_co_so:
            if duoc_si_co_so.co_so_kinh_doanh_id == current_co_so.id:
                return {
                    "msg": "Dược sĩ đã tồn tại trong cơ sở"
                }, HttpCode.BadRequest
            else:
                return {
                    "msg": "Dược sĩ hiện đang tồn tại trong cơ sở "+duoc_si_co_so.co_so_kinh_doanh.ten_coso
                }, HttpCode.BadRequest

        data["co_so_kinh_doanh_id"] = str(current_user.id)
        if not data.get("vai_tro"):
            return {
                "msg": "Thiếu dữ liệu vai trò"
            }, HttpCode.BadRequest
        if data.get("vai_tro") not in [0, 1]:
            return {
                "msg": "Dữ liệu vai trò nhập vào sai"
            }, HttpCode.BadRequest

        if data.get("vai_tro") == 0:
            if current_co_so.duoc_si_ctncm:
                return {
                    "msg": "Vai trò đã tồn tại, vui lòng sử dụng vai trò khác"
                }, HttpCode.BadRequest

        target = DuocSiCoSoSchema().load(data)

        db.session.add(target)
        db.session.commit()
        return {
            "msg": "Lưu thành công"
        }, HttpCode.OK
