from flask_restful import Resource
from flask import request
from application.extensions import db, pwd_context
from application.commons.pagination import paginate
# from application.models.danhmuc_vi_tri_hanh_nghe import ViTriHanhNghe
from application.models.danhmuc_van_bang_chuyen_mon import VanBangChuyenMon
from application.models.user import User

from application.schemas.danhmuc_van_bang_chuyen_mon import VanBangChuyenMonSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from flask_jwt_extended import (    
    jwt_required,
    current_user as user_jwt
)

from application.utils.validate.uuid_validator import is_valid_uuid


class VanBangChuyenMonResource(Resource):
    @jwt_required()
    def post(self):
        id = user_jwt.id
        user = User.query.filter(User.id == user_jwt.id).first()
        user.assigned_role
        
        if "admin" in [x.ten_en for x in user.assigned_role]:
            schema = VanBangChuyenMonSchema()
            vanbangchuyenmon = schema.load(request.json)
            db.session.add(vanbangchuyenmon)
            db.session.commit()
            return  schema.dump(vanbangchuyenmon)
        else:
            return {"errorCode":"EC18","msg":"Admin mới có quyền thêm!"},HttpCode.BadRequest

class VanBangChuyenMonGetList(Resource):
    @jwt_required()
    def post(self):
        schema = VanBangChuyenMonSchema(many =True)
        query = VanBangChuyenMon.query        
        data = request.json  
        if not data:
            query = query.order_by(VanBangChuyenMon.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_ten", None):
            search_ten = data["search_ten"]
            query = query.filter(VanBangChuyenMon.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(VanBangChuyenMon.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có văn bàng chuyên môn!"
            }, HttpCode.OK
        return res, HttpCode.OK
    
class VanBangChuyenMonById(Resource):
    @jwt_required()
    def put(self, id):
        schema = VanBangChuyenMonSchema()
        vanbangchuyenmon: VanBangChuyenMon = VanBangChuyenMon.query.filter(VanBangChuyenMon.id == id).first_or_404()
        ten = request.json.get('ten')
        if ten is not None:
            vanbangchuyenmon.ten_khong_dau = clean_string(ten)
        vanbangchuyenmon = schema.load(request.json, instance= vanbangchuyenmon)
        db.session.commit()
        return schema.dump(vanbangchuyenmon)
    
    @jwt_required()
    def delete(self, id):
        schema = VanBangChuyenMonSchema()
        vanbangchuyenmon: VanBangChuyenMon = VanBangChuyenMon.query.filter(VanBangChuyenMon.id == id).first_or_404()
        db.session.delete(vanbangchuyenmon)
        db.session.commit()
        return {"msg": "xóa thành công!"}, HttpCode.OK
class TimKiemTheoTen(Resource):
    
    def get(self):

        schema = VanBangChuyenMonSchema()
        van_bang= []
        van_bang_chuyen_mon = VanBangChuyenMon.query.all()
        for x in van_bang_chuyen_mon:
            van_bang.append(
                {
                    "label": x.ten,
                    "value":str(x.id)
                }
            )
        
        if van_bang is None:
            return {"errors": "No data"},  HttpCode.InternalError


        return {
            "results": {
                # "bang_cap": schema.dump(bang_cap),
                "van_bang":van_bang,
                # "tot_nghiep":tot_nghiep
            
            }
        }, HttpCode.OK   

        












