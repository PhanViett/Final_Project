from application.commons.pagination import paginate
from application.extensions import db
from application.models import Users
from application.models.tai_khoan import TaiKhoan
from application.schemas.nhan_vien import NguoiDungDisplaySchema, NhanVienUpdateSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from application.models.vai_tro import VaiTro


class QuanLyNguoiDungGetList(Resource):
    @ jwt_required()
    def post(self):
        schema = NguoiDungDisplaySchema(many=True)
        query = Users.query.filter(Users.active == True)
        data = request.json
        
        if not data:
            query = query.order_by(Users.ten_khong_dau.asc())
            return paginate(query, schema), HttpCode.OK

        elif data.get("search_key"):
            search_key = data["search_key"]
            query = query.filter(Users.ten_khong_dau.like(f"%{clean_string(search_key)}%"))

        query = query.order_by(Users.ten_khong_dau.asc())
        res = paginate(query, schema)

        if len(res["results"]) < 1:
        
            return {
                "msg": "Không có tên người dùng!!"
            }, HttpCode.OK

        return res, HttpCode.OK


class QuanLyNguoiDungCreate(Resource):
    @jwt_required()
    def post(self):
        
        ho = request.json.get('ho')
        ten = request.json.get('ten')
        tai_khoan = request.json.get('tai_khoan')
        mat_khau = request.json.get('mat_khau')
        email = request.json.get('email')
        dien_thoai = request.json.get('dien_thoai')
        
        is_exist = TaiKhoan.query.filter(TaiKhoan.tai_khoan == tai_khoan).first()

        if is_exist is not None:
            return jsonify({"status": "FAILED", "msg": "Tài khoản đã tồn tại!"}), HttpCode.BadRequest

        tai_khoan = TaiKhoan(tai_khoan=tai_khoan, mat_khau=mat_khau, dien_thoai=dien_thoai)
        db.session.add(tai_khoan)
        

        vai_tro = VaiTro.query.filter(VaiTro.ten_en == "user").first()
        user = Users(tai_khoan_id = tai_khoan.id, dien_thoai=dien_thoai, ho=ho, ten=ten, email=email)
        if vai_tro is not None:
            user.vai_tro_id = vai_tro.id
            user.assigned_role.append(vai_tro)
        db.session.add(user)

        db.session.commit()    

        return {"status": "SUCCESS", "msg": "Tạo mới người dùng thành công"}, HttpCode.Created


class QuanLyNguoiDungUpdate(Resource):
    @jwt_required()
    def post(self, id):
        schema = NhanVienUpdateSchema()
        user = Users.query.filter(Users.id == id, Users.active == True).first()
        if user is None: 
            return jsonify({"status": "FAILED", "msg": "Người dùng không tồn tại trong hệ thống"}), HttpCode.BadRequest

        req = {
            "ho": request.json.get("ho"),
            "ten": request.json.get('ten'),
            # "tai_khoan": request.json.get('tai_khoan'),
            # "mat_khau": request.json.get('mat_khau'),
            "email": request.json.get('email'),
            "dien_thoai": request.json.get('dien_thoai'), 
        }
       
        user = schema.load(req, instance=user)

        db.session.commit()    

        return {"status": "SUCCESS", "msg": "Tạo mới người dùng thành công"}, HttpCode.Created


class QuanLyNguoiDungDelete(Resource):
    @jwt_required()
    def delete(self, id):
        user = Users.query.filter(Users.id == id, Users.active == True).first()
        
        if user is None:
            return jsonify({"status": "FAILED", "msg": "Người dùng không tồn tại trong hệ thống"}), HttpCode.BadRequest
        db.session.delete(user)
        db.session.commit()

        return {"msg": "Xóa người dùng thành công!"}, HttpCode.OK