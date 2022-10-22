

from flask_restful import Resource
from flask import request
from application.extensions import db, pwd_context
from application.commons.pagination import paginate
from application.models.vai_tro import VaiTro
from application.schemas.vai_tro import VaiTroSchema, VaiTroSelectBoxSchema
from application.utils.helper.string_processing_helper import clean_string
# from application.models.danhmuc_vi_tri_hanh_nghe import ViTriHanhNghe
# from application.schemas.danhmuc_vi_tri_hanh_nghe import ViTriHanhNgheSchema
from application.utils.resource.http_code import HttpCode
from flask_jwt_extended import (
    jwt_required
)
# ok//


class VaiTroResource(Resource):

    def post(self):
        schema = VaiTroSchema()
        vaitro = schema.load(request.json)
        db.session.add(vaitro)
        db.session.commit()
        return schema.dump(vaitro)

# oke


class VaiTroGetList(Resource):
    # def get(self):
    #     schema = VaiTroSchema(many =True)
    #     vaitro = VaiTro.query
    #     return paginate(vaitro,schema)
    @jwt_required()
    def post(self):
        schema = VaiTroSchema(many=True)
        query = VaiTro.query
        data = request.json
        if not data:
            query = query.order_by(VaiTro.updated_at.desc())
            return paginate(query, schema), HttpCode.OK

        if data.get("search_ten"):
            search_ten = data["search_ten"]
            query = query.filter(VaiTro.ten_en.like(f"%{clean_string(search_ten)}%"))

        query = query.order_by(VaiTro.updated_at.desc())
        res = paginate(query, schema)
        if len(res["results"]) < 1:
            return {
                "msg": "Không có tên này!!"
            }, HttpCode.OK

        return res, HttpCode.OK


class VaiTroSelectList(Resource):
    @jwt_required()
    def get(self):
        schema = VaiTroSelectBoxSchema(many=True)
        query = VaiTro.query
        return paginate(query=query, schema=schema)
# oke


class VaiTroById(Resource):
    @jwt_required()
    def put(self, id):
        schema = VaiTroSchema()
        vaitro: VaiTro = VaiTro.query.filter(VaiTro.id == id).first()
        # if vitrihanhnghe in (ViTriHanhNghe.id == id):
        #     return {"msg": "có dữ liệu"}, HttpCode.OK

        # if vitrihanhnghe is None:
        #     return {"msg": "không có dữ liệu"}, HttpCode.NotFound
        vaitro = schema.load(request.json, instance=vaitro)
        db.session.commit()
        return {"msg": "có dữ liệu",
                "vaitro": schema.dump(vaitro)}, HttpCode.OK,

# oke
    def get(self, id):
        schema = VaiTroSchema()
        vaitro: VaiTro = VaiTro.query.filter(VaiTro.id == id).first_or_404()
        return schema.dump(vaitro)
# oke

    def delete(self, id):
        schema = VaiTroSchema()
        vaitro: VaiTro = VaiTro.query.filter(VaiTro.id == id).first_or_404()
        db.session.delete(vaitro)
        db.session.commit()
        return {"msg": "Xóa thành công"}, HttpCode.OK
