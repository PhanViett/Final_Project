from flask_restful import Resource
from flask import request, jsonify
from application.extensions import db, pwd_context
from application.models.danhmuc_thu_tuc import DanhMucThuTuc
from application.models.user import User

from application.schemas.danhmuc_thu_tuc import DanhMucThuTucSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from application.commons.pagination import paginate
from flask_jwt_extended import (    
    jwt_required,
    current_user as  user_jwt,
)
class ThuTucResource(Resource):
    @jwt_required()
    def post(self):
        id = user_jwt.id
        user = User.query.filter(User.id == user_jwt.id).first()
        user.assigned_role
        
        if "admin" in [x.ten_en for x in user.assigned_role]:
            schema = DanhMucThuTucSchema()
            thu_tuc = schema.load(request.json)
            db.session.add(thu_tuc)
            db.session.commit()
            return  schema.dump(thu_tuc)
        else:
            return {"errorCode":"EC18","msg":"Admin mới có quyền thêm!"},HttpCode.BadRequest


class ThuTucGetList(Resource):
    @jwt_required()
    def post(self):
        schema = DanhMucThuTucSchema(many =True)
        query = DanhMucThuTuc.query        
        data = request.json  
        if not data:
            query = query.order_by(DanhMucThuTuc.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_ten", None):
            search_ten = data["search_ten"]
            query = query.filter(DanhMucThuTuc.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(DanhMucThuTuc.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có thủ tục! "
            }, HttpCode.BadRequest
        return res, HttpCode.OK

class ThuTucGetByUser(Resource):
    @jwt_required()
    def post(self):
        schema = DanhMucThuTucSchema(many=True)
        
        user = User.query.filter(User.id == user_jwt.id).first()
        user.assigned_role
        
        if "duocsi" in [x.ten_en for x in user.assigned_role]:
            if user.da_cap_chung_chi == True:
                query = DanhMucThuTuc.query.filter(DanhMucThuTuc.doi_tuong == '1', DanhMucThuTuc.trang_thai == False)
                return paginate(query, schema)
            if user.da_cap_chung_chi == False:
                query = DanhMucThuTuc.query.filter(DanhMucThuTuc.doi_tuong == '1', DanhMucThuTuc.trang_thai == True)
                return paginate(query, schema)
        if "tochuc" in [x.ten_en for x in user.assigned_role]:
            query = DanhMucThuTuc.query.filter(DanhMucThuTuc.doi_tuong == '2', DanhMucThuTuc.trang_thai == False)
            return paginate(query, schema)
        if "chuyenvien" in [x.ten_en for x in user.assigned_role]:
            query = DanhMucThuTuc.query.filter(DanhMucThuTuc.doi_tuong == '1')
            return paginate(query, schema)

        return {"msg":"Không thuộc đối tượng chọn loại thủ tục"}, HttpCode.BadRequest

class ThuTucById(Resource):
    @jwt_required()
    def put(self, id):
        schema = DanhMucThuTucSchema()
        thutuc: DanhMucThuTuc = DanhMucThuTuc.query.filter(DanhMucThuTuc.id == id).first()
        ten = request.json.get('ten')
        if ten is not None:
            thutuc.ten_khong_dau = clean_string(ten)
        if thutuc is None:
            return {"msg": "danh muc ko ton tai"}, HttpCode.BadRequest
        thutuc = schema.load(request.json, instance=thutuc)
        db.session.commit()
        return schema.dump(thutuc)
    
    @jwt_required()
    def get(self,id):
        schema = DanhMucThuTucSchema()
        thutuc: DanhMucThuTuc = DanhMucThuTuc.query.filter(DanhMucThuTuc.id == id).first_or_404()
        return schema.dump(thutuc)
    @jwt_required()
    def delete(self, id):
        schema = DanhMucThuTucSchema()
        thutuc: DanhMucThuTuc = DanhMucThuTuc.query.filter(DanhMucThuTuc.id == id).first_or_404()
        db.session.delete(thutuc)
        db.session.commit()
        return {"msg": "xóa thành công"}, HttpCode.OK
  