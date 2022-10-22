

from flask_restful import Resource
from flask import request
from application.extensions import db, pwd_context
# from application.models.danhmuc_noi_tot_nghiep import NoiTotNghiep
from application.models.danhmuc_pham_vi_hoat_dong_kinh_doanh import PhamViHoatDongKinhDoanh
from application.commons.pagination import paginate
from application.models.user import User
from application.schemas.danhmuc_pham_vi_hoat_dong_kinh_doanh import PhamVihoatDongKinhDoanhSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode

from flask_jwt_extended import (    
    jwt_required,
    current_user as user_jwt,
)

class PhamViHoatDongKinhDoanhResource(Resource):
    
    @jwt_required()
    def post(self):
        user = User.query.filter(User.id == user_jwt.id).first()
        user.assigned_role
        
        if "admin" in [x.ten_en for x in user.assigned_role]:
            schema = PhamVihoatDongKinhDoanhSchema()
            hoat_dong_kinh_doanh = schema.load(request.json)
            db.session.add(hoat_dong_kinh_doanh)
            db.session.commit()
            return  schema.dump(hoat_dong_kinh_doanh)
        else:
            return {"errorCode":"EC18","msg":"Admin mới có quyền thêm!"},HttpCode.BadRequest

# oke
class PhamViHoatDongKinhDoanhGetList(Resource):
    @jwt_required()
    def post(self):
        schema = PhamVihoatDongKinhDoanhSchema(many =True)
        query = PhamViHoatDongKinhDoanh.query        
        data = request.json  
        if not data:
            query = query.order_by(PhamViHoatDongKinhDoanh.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        
        if data.get("search_ten", None):
            search_ten = data["search_ten"]
            query = query.filter(PhamViHoatDongKinhDoanh.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(PhamViHoatDongKinhDoanh.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có phạm vi hoạt động kinh doanh!"
            }, HttpCode.OK
        return res, HttpCode.OK
    
class PhamViHoatDongKinhDoanhById(Resource):
    @jwt_required()
    def put(self, id):
        schema = PhamVihoatDongKinhDoanhSchema()
        phamvihoatdongkinhdoanh: PhamViHoatDongKinhDoanh = PhamViHoatDongKinhDoanh.query.filter(PhamViHoatDongKinhDoanh.id == id).first()
        ten = request.json.get('ten')
        if ten is not None:
            phamvihoatdongkinhdoanh.ten_khong_dau = clean_string(ten)
        phamvihoatdongkinhdoanh = schema.load(request.json, instance= phamvihoatdongkinhdoanh)
        db.session.commit()
        return schema.dump(phamvihoatdongkinhdoanh)

# oke
    @jwt_required()
    def get(self,id):
        schema = PhamVihoatDongKinhDoanhSchema()
        phamvihoatdongkinhdoanh: PhamViHoatDongKinhDoanh = PhamViHoatDongKinhDoanh.query.filter(PhamViHoatDongKinhDoanh.id == id).first_or_404()
        return schema.dump(phamvihoatdongkinhdoanh)
# oke
    @jwt_required()
    def delete(self, id):
        schema = PhamVihoatDongKinhDoanhSchema()
        phamvihoatdongkinhdoanh: PhamViHoatDongKinhDoanh = PhamViHoatDongKinhDoanh.query.filter(PhamViHoatDongKinhDoanh.id == id).first_or_404()
        db.session.delete(phamvihoatdongkinhdoanh)
        db.session.commit()
        return {"msg": "xóa thành công"}, HttpCode.OK
class TimKiemTheoTen(Resource):
    @jwt_required()
    def post(self):
        schema = PhamVihoatDongKinhDoanhSchema(many =True)
        ten = request.json.get("ten")
        query = PhamViHoatDongKinhDoanh.query             
        if not request.json:
            query = query.order_by(PhamViHoatDongKinhDoanh.updated_at.desc())
            return paginate(query, schema), HttpCode.OK
        

        if "trang_thai" in request.json:
            if request.json.get("trang_thai") != None:
                query = query.filter(
                    PhamViHoatDongKinhDoanh.trang_thai == request.json.get("trang_thai")
                )  
        if "ten" in request.json:
            query = query.filter(PhamViHoatDongKinhDoanh.ten_khong_dau.like(f"%{clean_string(ten)}%"))     
        if len(query.all()) <= 0:
             return {"msg":"Phạm vi hoạt động kinh doanh không có!",
                     "results": schema.dump(query)}, HttpCode.OK
        return paginate(query,schema), HttpCode.OK      

        












