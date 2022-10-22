

from datetime import datetime
from flask_restful import Resource
from flask import request
from application.extensions import db, pwd_context
from application.commons.pagination import paginate
from application.models.bang_thong_bao import ThongBao
from application.models.vai_tro import VaiTro
from application.schemas.bang_thong_bao import ThongBaoSchema
from application.schemas.vai_tro import VaiTroSchema
# from application.models.danhmuc_vi_tri_hanh_nghe import ViTriHanhNghe
# from application.schemas.danhmuc_vi_tri_hanh_nghe import ViTriHanhNgheSchema
from application.utils.resource.http_code import HttpCode
from flask_jwt_extended import (
    current_user,
    jwt_required
)
# ok//


class ThongBaoResource(Resource):
    @jwt_required()
    def post(self):
        schema = ThongBaoSchema()
        thongbao = schema.load(request.json)
        db.session.add(thongbao)
        db.session.commit()
        return schema.dump(thongbao)


class ThongBaoGetList(Resource):
    @jwt_required()
    def get(self):
        schema = ThongBaoSchema(many=True)
        thongbao = ThongBao.query.filter(ThongBao.nhan_vien_id == str(
            current_user.id)).order_by(ThongBao.notify_at.desc())
        res = paginate(thongbao, schema)
        res["total_unread"] = sum(thong_bao["read_at"] is None for thong_bao in res["results"])
        return res, HttpCode.OK


class ThongBaoDetails(Resource):
    @jwt_required()
    def get(self, id):
        schema = ThongBaoSchema()
        thong_bao = ThongBao.query.filter(ThongBao.id == id).first_or_404()
        return {
            "msg": "Thành công",
            "result": schema.dump(thong_bao)
        }, HttpCode.OK

    @jwt_required()
    def delete(self, id):
        schema = ThongBaoSchema()
        thongbao: ThongBao = ThongBao.query.filter(ThongBao.id == id).first_or_404()
        db.session.delete(thongbao)
        db.session.commit()
        return {"msg": "Xóa thành công"}, HttpCode.OK

    @jwt_required()
    def put(self, id):
        schema = ThongBaoSchema()
        thongbao: ThongBao = ThongBao.query.filter(ThongBao.id == id).first()
        # if vitrihanhnghe in (ViTriHanhNghe.id == id):
        #     return {"msg": "có dữ liệu"}, HttpCode.OK
        # if vitrihanhnghe is None:
        #     return {"msg": "không có dữ liệu"}, HttpCode.NotFound
        thongbao = schema.load(request.json, instance=thongbao)
        db.session.commit()
        return {"msg": "Thành công",
                "results": schema.dump(thongbao)}, HttpCode.OK,


class ThongBaoRead(Resource):
    def put(self, id):
        thong_bao: ThongBao = ThongBao.query.get_or_404(id)
        thong_bao.read_at = datetime.now().timestamp()
        db.session.commit()
        return {
            "msg": "Thành công",
            "results": int(thong_bao.read_at)
        }
