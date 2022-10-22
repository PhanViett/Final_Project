from marshmallow import ValidationError
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from application.controllers.duoc_si import chung_chi_hanh_nghe
from application.models.danhmuc_thu_tuc import DanhMucThuTuc
from application.models.danhmuc_vi_tri_hanh_nghe import ViTriHanhNghe
from application.models.yeu_cau_chung_chi_hanh_nghe import YeuCauChungChiHanhNghe
from application.models.yeu_cau_dang_ky_kinh_doanh import YeuCauDangKyKinhDoanh
from application.schemas.yeu_cau_chung_chi_hanh_nghe import YeuCauChungChiHanhNgheSchema
from application.schemas.yeu_cau_dang_ky_kinh_doanh import YeuCauDangKyKinhDoanhSchema
from application.schemas.co_so_kinh_doanh import CoSoKinhDoanhSchema
from application.utils.helper.generate_so_thu_tu import generate_number
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
from application.extensions import db
from application.controllers.auth.helpers import to_dict


class DangKyKinhDoanhPost(Resource):

    @jwt_required()
    def post(self):

        schema = YeuCauDangKyKinhDoanhSchema(many=True)

        req = {
            "thu_tuc_id": request.json.get("thu_tuc_id"),
        }

        try:
            dang_ky = schema.load(req)
            dang_ky.nhan_vien_id = current_user.id
            dang_ky.trang_thai_ho_so = "1"
            dang_ky.doi_tuong = to_dict(current_user)
            thu_tuc = DanhMucThuTuc.query.filter(DanhMucThuTuc.id == request.json.get("thu_tuc_id")).first()
            if thu_tuc is None:
                return {"errors": "Thủ tục không tồn tại"}, HttpCode.BadRequest
            try:
                if thu_tuc.doi_tuong != '2':
                    return {"errors": "Đối tượng không thuộc thủ tục thực hiện"}, HttpCode.BadRequest
            except:
                return {"errors": "!!!!!!!!!!!"}, HttpCode.InternalError
            if thu_tuc.ma_thu_tuc == 'TT006':
                db.session.add(dang_ky)
                db.session.commit()

        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest

        return {"msg": "Yêu Cầu Đăng Ký Kinh Doanh tạo thành công", "results": schema.dump(dang_ky)}, HttpCode.Created


class YCGPKDYeuCauMoi(Resource):
    def post(self):
        data = request.json
        if not data.get("thu_tuc_id", False):
            return {"msg": "Thiếu thủ tục nhập vào"}, HttpCode.BadRequest
        target_thu_tuc = DanhMucThuTuc.query.get(data["thu_tuc_id"])
        if not target_thu_tuc:
            return {"msg": "Thủ tục không tồn tại"}, HttpCode.OK
        new_ycgpkd = YeuCauDangKyKinhDoanh(co_so_kinh_doanh_id=current_user.id, thu_tuc_id=data["thu_tuc_id"])
        db.session.add(new_ycgpkd)
        db.session.commit()
        return {
            "msg": "Tạo thủ tục cấp mới thành công",
            "results": {
                "thu_tuc_id": str(new_ycgpkd.id)
            }
        }, HttpCode.OK


class YCGPKDXuLyThongTin(Resource):
    def put(self, id):  # Lưu thông tin
        data = request.json
        target_ycgpkd: YeuCauChungChiHanhNghe = YeuCauDangKyKinhDoanh.query.get_or_404(id)
        if data.get("pham_vi_kinh_doanh", False):
            target_ycgpkd.pham_vi_chuyen_mon = data.get("pham_vi_chuyen_mon")
