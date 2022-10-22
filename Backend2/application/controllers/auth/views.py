from flask_jwt_extended import decode_token
from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    current_user as user_jwt,
    current_user
)
from requests import delete
from marshmallow import ValidationError
from application.models.tinh_thanh import TinhThanh
from application.models.quan_huyen import QuanHuyen
from application.models.xa_phuong import XaPhuong
from application.models.tai_khoan import TaiKhoan
from application.models.vai_tro import VaiTro
from application.schemas.nhan_vien import QuanLyNguoiDungSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from application.schemas import NhanVienSchema, CoSoKinhDoanhSchema
from application.models import User, CoSoKinhDoanh

import redis
from datetime import datetime, timedelta
import os
import json
from application.utils.helper.string_processing_helper import clean_string
ACCESS_EXPIRES = timedelta(days=365)

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

# jwt_redis_blocklist = redisdb


@blueprint.route("/get_current_user", methods=["POST"])
@jwt_required()
def get_current_user():
    schema = NhanVienSchema()
    user = User.query.filter(User.id == user_jwt.id).first()
    return schema.dump(user)


@blueprint.route("/register_notify", methods=["POST"])
@jwt_required()
def register_notify():
    try:
        access_token = request.headers.get('Authorization')
        access_token = access_token.split("Bearer ")[1]
        expires: int = int(decode_token(access_token)["exp"] - datetime.now().timestamp())
        fcm_token = request.headers.get('fcm_token')
        # if redisdb.exists("fcm_token:"+str(current_user.id)+":"+fcm_token):
        #     return {
        #         "msg": "Tài khoản đã đăng ký"
        #     }, HttpCode.OK
        # if redisdb.exists("fcm_token:"+"*:"+fcm_token):
        #     exist_keys = redisdb.keys("fcm_token:"+"*"+":"+fcm_token)
        #     print(exist_keys)
        #     redisdb.delete(*exist_keys)
        # redisdb.set("fcm_token:"+str(current_user.id)+":"+fcm_token, fcm_token, ex=expires)
        return {
            "msg": "Đăng ký thông báo thành công"
        }, HttpCode.OK
    except Exception as e:
        print(" ".join(e.args))
        return {
            "msg": "Đăng ký thông báo thất bại"
        }, HttpCode.InternalError


@ blueprint.route("/logout", methods=["POST"])
@ jwt_required()
def logout():
  return Flase

@ blueprint.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, HttpCode.BadRequest

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return (
            jsonify({"errorCode": "EC01", "msg": "Missing username or password"}),
            HttpCode.BadRequest,
        )

    # todo VALIDATE tai_khoan
    tai_khoan: TaiKhoan = TaiKhoan.query.filter(TaiKhoan.tai_khoan == username).first()
    if not tai_khoan or not pwd_context.verify(password, tai_khoan.mat_khau):
        return (
            jsonify(
                {"errorCode": "EC01", "msg": "Username hoặc mật khẩu không chính xác"}
            ),
            HttpCode.BadRequest,
        )

    target = None
    schema = None
    if tai_khoan.type == 0:
        target = User.query.filter(User.tai_khoan_id == tai_khoan.id).first()
        schema = NhanVienSchema()
    elif tai_khoan.type == 1:
        target = CoSoKinhDoanh.query.filter(CoSoKinhDoanh.taikhoan_id == tai_khoan.id).first()
        schema = CoSoKinhDoanhSchema()

    #  todo APPLY TOKEN
    access_token = create_access_token(identity=str(target.id), additional_claims={"account_type": tai_khoan.type})
    refresh_token = create_refresh_token(identity=str(target.id), additional_claims={"account_type": tai_khoan.type})
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

    user_data: dict = schema.dump(target)
    user_data["tai_khoan"] = username

    # RETURN USER's ROLE
    # vai_tro: VaiTro = nhan_vien.assigned_role
    # if vai_tro:
    #     user_data.update({"ten_vai_tro": nhan_vien.assigned_role.ten})
    # else:
    #     user_data.update({"ten_vai_tro": None})
    # todo SET LAST LOGIN FOR tai_khoan
    tai_khoan.last_login_at = datetime.now()
    db.session.commit()
    ret = {
        "msg": "Đăng nhập thành công",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "userInfo": user_data,
    }
    return ret, HttpCode.OK


@ blueprint.route("/register", methods=["POST"])
def register():
    schema = QuanLyNguoiDungSchema()

    tai_khoan = request.json.get('tai_khoan')
    mat_khau = request.json.get('mat_khau')
    dien_thoai = request.json.get('dien_thoai')
    vai_tro_id = request.json.get('vai_tro_id')

    if mat_khau is None or mat_khau.strip() == '':
        return jsonify({"error_code": "REGISTER_FAILED", "error_message": "Mật khẩu không hợp lệ!"}), HttpCode.BadRequest

    if tai_khoan is None or tai_khoan == '':
        return jsonify({"error_code": "REGISTER_FAILED", "error_message": "Tài khoản không hợp lệ!"}), HttpCode.BadRequest

    is_valid = TaiKhoan.query.filter(TaiKhoan.tai_khoan == tai_khoan).first()
    if is_valid is not None:
        return jsonify({"error_code": "REGISTER_FAILED", "error_message": "Tài khoản đã tồn tại!"}), HttpCode.BadRequest
    if vai_tro_id is not None:
        vai_tro_check = VaiTro.query.filter(VaiTro.id == vai_tro_id).first()
        if vai_tro_check is None:
            return jsonify({"error_code": "REGISTER_FAILED", "error_message": "Vai trò không tồn tại!"}), HttpCode.BadRequest
        else:
            user = TaiKhoan(tai_khoan=tai_khoan, mat_khau=mat_khau, dien_thoai=dien_thoai)
            if vai_tro_check.ten_en == 'tochuc':
                user.type = 1
            elif vai_tro_check.ten_en == 'duocsi':
                user.type = 0
            db.session.add(user)
            db.session.commit()
            if vai_tro_check.ten_en == 'tochuc':
                co_so = CoSoKinhDoanh(taikhoan_id=user.id, da_cap_giay_phep=False,
                                      dienthoai_coso=user.dien_thoai, ten_coso="")
                co_so.assigned_role.append(vai_tro_check)
                db.session.add(co_so)
                db.session.commit()
            elif vai_tro_check.ten_en == 'duocsi':
                nhan_vien = User(tai_khoan_id=user.id, da_cap_chung_chi=False,
                                 dien_thoai=user.dien_thoai, ho="", ten="")
                nhan_vien.assigned_role.append(vai_tro_check)
                db.session.add(nhan_vien)
                db.session.commit()
                return {"msg": "Tạo mới người dùng thành công", "nguoi_dung": schema.dump(nhan_vien)}, HttpCode.Created


@blueprint.route("/dang-ky", methods=["POST"])
@jwt_required(refresh=True)
def ládfjdlsfads():
    schema = QuanLyNguoiDungSchema()

    req = {
        "avatar_url": request.form.get("avatar_url"),
        "ho": request.form.get("ho"),
        "ten": request.form.get("ten"),
        "ngay_sinh": request.form.get("ngay_sinh"),
        "gioi_tinh": request.form.get("gioi_tinh"),
        "ma_cong_dan": request.form.get("ma_cong_dan"),
        "ngay_cap": request.form.get("ngay_cap"),
        "noi_cap": request.form.get("noi_cap"),
        "dien_thoai": request.form.get("dien_thoai"),
        "email": request.form.get("email"),
        "tinh_thanh_id": request.form.get("tinh_thanh_id"),
        "quan_huyen_id": request.form.get("quan_huyen_id"),
        "xa_phuong_id": request.form.get("xa_phuong_id"),
        "so_nha": request.form.get("so_nha"),
        "tinh_thanh_hien_nay_id": request.form.get("tinh_thanh_hien_nay_id"),
        "quan_huyen_hien_nay_id": request.form.get("quan_huyen_hien_nay_id"),
        "xa_phuong_hien_nay_id": request.form.get("xa_phuong_hien_nay_id"),
        "so_nha_thuong_tru": request.form.get("so_nha_thuong_tru"),
    }

    try:
        tai_khoan = clean_string(req["ho"] + req["ten"])

        for x in range(100):
            checkTaiKhoan = TaiKhoan.query.filter(TaiKhoan.tai_khoan == tai_khoan).first()
            if checkTaiKhoan is not None:
                tai_khoan = clean_string(req["ho"] + req["ten"]) + str(x)
            else:
                break

        tai_khoan = TaiKhoan(tai_khoan=tai_khoan, mat_khau="12345678", dien_thoai=request.form.get('dien_thoai'))
        tai_khoan.type = 0

        db.session.add(tai_khoan)
        db.session.commit()

        quan_ly_nguoi_dung: User = schema.load(req)

        vai_tro_check = VaiTro.query.filter(VaiTro.id == "96e2a4d8-6e15-4309-a91d-17ab26533552").first()
        quan_ly_nguoi_dung.assigned_role.append(vai_tro_check)

        ho_ten = req["ho"] + " " + req["ten"]

        quan_ly_nguoi_dung.tai_khoan_id = tai_khoan.id
        quan_ly_nguoi_dung.ho_ten = ho_ten
        quan_ly_nguoi_dung.ten_khong_dau = clean_string(ho_ten)
        quan_ly_nguoi_dung.da_cap_chung_chi = False
        quan_ly_nguoi_dung.dien_thoai = req["dien_thoai"]
        quan_ly_nguoi_dung.created_by = current_user.id

        # dia chi thuong tru
        so_nha_thuong_tru = request.form.get("so_nha_thuong_tru")
        quan_huyen_id = request.form.get("quan_huyen_id")
        xa_phuong_id = request.form.get("xa_phuong_id")
        tinh_thanh_id = request.form.get("tinh_thanh_id")
        quan_huyen_query = QuanHuyen.query.filter(QuanHuyen.id == quan_huyen_id).first()
        xa_phuong_query = XaPhuong.query.filter(XaPhuong.id == xa_phuong_id).first()
        tinh_thanh_query = TinhThanh.query.filter(TinhThanh.id == tinh_thanh_id).first()

        # cho o hien nay
        so_nha = request.form.get("so_nha")
        quan_huyen_hien_nay_id = request.form.get("quan_huyen_hien_nay_id")
        xa_phuong_hien_nay_id = request.form.get("xa_phuong_hien_nay_id")
        tinh_thanh_hien_nay_id = request.form.get("tinh_thanh_hien_nay_id")
        quan_huyen_hien_nay_query = QuanHuyen.query.filter(QuanHuyen.id == quan_huyen_hien_nay_id).first()
        xa_phuong_hien_nay_query = XaPhuong.query.filter(XaPhuong.id == xa_phuong_hien_nay_id).first()
        tinh_thanh_hien_nay_query = TinhThanh.query.filter(TinhThanh.id == tinh_thanh_hien_nay_id).first()

        # add ho khau thuong tru
        if so_nha_thuong_tru is not None and so_nha_thuong_tru != "":
            dia_chi_thuong_tru = so_nha_thuong_tru + ", " + xa_phuong_query.ten + \
                ", " + quan_huyen_query.ten + ", " + tinh_thanh_query.ten
        else:
            dia_chi_thuong_tru = xa_phuong_query.ten + ", " + quan_huyen_query.ten + ", " + tinh_thanh_query.ten
        quan_ly_nguoi_dung.dia_chi_thuong_tru = dia_chi_thuong_tru

        # add cho o hien nay
        if so_nha is not None and so_nha != "":
            dia_chi = so_nha + ", " + xa_phuong_hien_nay_query.ten + ", " + \
                quan_huyen_hien_nay_query.ten + ", " + tinh_thanh_hien_nay_query.ten
        else:
            dia_chi = xa_phuong_hien_nay_query.ten + ", " + quan_huyen_hien_nay_query.ten + ", " + tinh_thanh_hien_nay_query.ten
        quan_ly_nguoi_dung.dia_chi = dia_chi

        avatar_url = request.files.get("avatar_url")
        if avatar_url is not None:
            try:
                quan_ly_nguoi_dung.avatar_url = avatar_url
            except:
                return {"errors": "Tải file thất bại"},  HttpCode.InternalError

    except ValidationError as err:
        return {"errors": err.messages},  HttpCode.BadRequest

    db.session.commit()
    return {"msg": "Cập nhật thành công", "nguoi_dung": schema.dump(quan_ly_nguoi_dung)}, HttpCode.Created


@blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Get an access token from a refresh token
    ---
    post:
      tags:
        - auth
      summary: Get an access token
      description: Get an access token by using a refresh token in the `Authorization` header
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myaccesstoken
        400:
          description: bad request
        401:
          description: unauthorized
    """
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {"access_token": access_token}
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    return jsonify(ret), HttpCode.OK


@blueprint.route("/revoke-access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    """Revoke an access token

    ---
    delete:
      tags:
        - auth
      summary: Revoke an access token
      description: Revoke an access token
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    return jsonify({"message": "token revoked"}), HttpCode.OK


@blueprint.route("/revoke-refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    """Revoke a refresh token, used mainly for logout

    ---
    delete:
      tags:
        - auth
      summary: Revoke a refresh token
      description: Revoke a refresh token, used mainly for logout
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify({"message": "token revoked"}), HttpCode.OK


@blueprint.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    """Change Password

    ---
     put:
        tags:
          - auth
        summary: Change Password
        description: Change password fors nhan_vien
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  old_password:
                    type: string
                    example: P4$$w0rd!
                    required: true
                  new_password:
                    type: string
                    example: PaSsW0rD@
                    required: true
                  retype_password:
                    type: string
                    example: PaSsW0rD@
                    required: true
        responses:
          200:
            description: change password successfully
          400:
            description: bad request
    """
    method_decorators = [jwt_required()]
    password = user_jwt.tai_khoan.mat_khau
    old_password = request.json.get("old_password", None)
    new_password = request.json.get("new_password", None)
    retype_password = request.json.get("retype_password", None)

    if pwd_context.verify(old_password, password) is False:
        return (
            jsonify({"msg": "Mật khẩu cũ không đúng."}),
            HttpCode.BadRequest,
        )

    if new_password != retype_password:
        return jsonify({"msg": "Mật khẩu xác nhận không trùng khớp."}), HttpCode.BadRequest

    user = TaiKhoan.query.filter(TaiKhoan.id == user_jwt.tai_khoan_id).first()
    user.mat_khau = pwd_context.hash(new_password)
    db.session.commit()

    return jsonify({"msg": "Thay đổi mật khẩu thành công."}), HttpCode.OK


def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    if token_in_redis is not None:
        token_in_redis = json.loads(token_in_redis)
        return token_in_redis.get("revoked", False)
    return False
