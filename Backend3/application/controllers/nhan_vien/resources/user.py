from application.commons.pagination import paginate
from application.extensions import db
from application.models import Users
from application.models.tai_khoan import TaiKhoan
from application.schemas.nhan_vien import NguoiDungDisplaySchema, NhanVienUpdateSchema, NhanVienRecordSchema
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
        query = Users.query.filter(Users.status == True)
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
        # elif len(res["results"]) >= 1:
        #     for x in res["results"]:
        #         a = TaiKhoan.query.filter(TaiKhoan.user_id == x["id"]).first()
        #         x["tai_khoan"] = a.tai_khoan

                
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
            return {"status": "FAILED", "msg": "Tài khoản đã tồn tại!"}, HttpCode.BadRequest

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
    def put(self, id):

        schema = NhanVienUpdateSchema(partial=True)
        user = Users.query.filter(Users.id == id, Users.status == True).first()
        if user is None: 
            return jsonify({"status": "FAILED", "msg": "Người dùng không tồn tại trong hệ thống"}), HttpCode.BadRequest

        req = {
            "avatar_url": request.form.get('avatar_url'),
            "ho": request.form.get('ho'),
            "ten": request.form.get('ten'),
            "ngay_sinh": request.form.get('ngay_sinh'),
            "gioi_tinh": request.form.get('gioi_tinh'),
            "ma_cong_dan": request.form.get('ma_cong_dan'),
            "ngay_cap": request.form.get('ngay_cap'),
            "noi_cap": request.form.get('noi_cap'),
            "dien_thoai": request.form.get('dien_thoai'),
            "email": request.form.get('email'),
            "tinh_thanh_hien_nay_id": request.form.get('tinh_thanh_hien_nay_id'),
            "quan_huyen_hien_nay_id": request.form.get('quan_huyen_hien_nay_id'),
            "xa_phuong_hien_nay_id": request.form.get('xa_phuong_hien_nay_id'),
            "so_nha_hien_nay": request.form.get('so_nha_hien_nay'),
            "tinh_thanh_thuong_tru_id": request.form.get('tinh_thanh_thuong_tru_id'),
            "quan_huyen_thuong_tru_id": request.form.get('quan_huyen_thuong_tru_id'),
            "xa_phuong_thuong_tru_id": request.form.get('xa_phuong_thuong_tru_id'),
            "so_nha_thuong_tru": request.form.get('so_nha_thuong_tru'),

        }
       
        user = schema.load(req, instance=user)
        
        db.session.commit()    

        return {"status": "SUCCESS", "msg": "Cập nhật người dùng thành công", "results": schema.dump(user)}, HttpCode.Created


class QuanLyNguoiDungDelete(Resource):
    @jwt_required()
    def delete(self, id):
        user = Users.query.filter(Users.id == id, Users.status == True).first()
        
        if user is None:
            return jsonify({"status": "FAILED", "msg": "Người dùng không tồn tại trong hệ thống"}), HttpCode.BadRequest
        db.session.delete(user)
        db.session.commit()

        return {"msg": "Xóa người dùng thành công!"}, HttpCode.OK


class GetUserInfo(Resource):
    @jwt_required()
    def get(self, id):
        schema = NhanVienRecordSchema()
        user = Users.query.filter(Users.id == id, Users.status == True).first()
        
        if user is None: 
            return jsonify({"status": "FAILED", "msg": "Người dùng không tồn tại trong hệ thống"}), HttpCode.BadRequest
        else:
            result = schema.dump(user)
        return result, HttpCode.OK


class UpdateUserStatic(Resource):
    @jwt_required()
    def put(self, id):
        schema = NhanVienRecordSchema()
        user = Users.query.filter(Users.id == id, Users.status == True).first()

        req = {
            "height": request.form.get('height'),
            "weight": request.form.get('weight'),
            "tuoi": request.form.get('tuoi'),
            "gioi_tinh": request.form.get('gioi_tinh'),
            "chol": request.form.get('chol'),
            "gluc": request.form.get('gluc'),
            "smoke": request.form.get('smoke'),
            "alco": request.form.get('alco'),
            "active": request.form.get('active'),
        }

        user = schema.load(req, instance=user)
        db.session.commit()

        return {"status": "SUCCESS", "msg": "Cập nhật thông tin thành công", "results": schema.dump(user)}, HttpCode.OK