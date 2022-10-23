import json
import os
from datetime import timedelta
import redis
from application.controllers.auth.helpers import (add_token_to_database,
                                                  is_token_revoked,
                                                  revoke_token)
from application.extensions import apispec, db, jwt, pwd_context

from application.models import Users
from application.models.tai_khoan import TaiKhoan
from application.models.vai_tro import VaiTro
from application.schemas.nhan_vien import NhanVienSchema
from application.utils.helper.convert_timestamp_helper import get_current_time
from application.utils.helper.role_helper import get_user_permissions
from application.utils.resource.http_code import HttpCode
from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import current_user as user_jwt
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

ACCESS_EXPIRES = timedelta(days=365)

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

jwt_redis_blocklist = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=os.getenv("REDIS_DB"),
    decode_responses=os.getenv("REDIS_DECODE_RESPONSES"),
)


@blueprint.route("/login", methods=["POST"])
def login():

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    if not username or not password:
        return (
            jsonify({"errorCode": "EC01", "msg": "Missing username or password"}),
            HttpCode.BadRequest,
        )

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

    target = Users.query.filter(Users.tai_khoan_id == tai_khoan.id).first()
    schema = NhanVienSchema()

    #  todo APPLY TOKEN
    access_token = create_access_token(identity=str(target.id), additional_claims={"account_type": tai_khoan.type})
    refresh_token = create_refresh_token(identity=str(target.id), additional_claims={"account_type": tai_khoan.type})
    # add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    # add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

    user_data: dict = schema.dump(target)
    user_data["tai_khoan"] = username

    tai_khoan.last_login_at = get_current_time("int")
    db.session.commit()
    ret = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "userInfo": user_data,
    }
    return ret, HttpCode.OK


@blueprint.route("/register", methods=["POST"])
def register():

    ho = request.json.get('ho')
    ten = request.json.get('ten')
    tai_khoan = request.json.get('tai_khoan')
    mat_khau = request.json.get('mat_khau')
    email = request.json.get('email')
    dien_thoai = request.json.get('dien_thoai')

    if tai_khoan is None or tai_khoan == '':
        return jsonify({"error_code": "REGISTER_FAILED", "error_message": "Tài khoản không hợp lệ!"}), HttpCode.BadRequest
    if mat_khau is None or mat_khau.strip() == '':
        return jsonify({"error_code": "REGISTER_FAILED", "error_message": "Mật khẩu không hợp lệ!"}), HttpCode.BadRequest
    
    is_exist = TaiKhoan.query.filter(TaiKhoan.tai_khoan == tai_khoan).first()

    if is_exist is not None:
        return jsonify({"error_code": "REGISTER_FAILED", "error_message": "Tài khoản đã tồn tại!"}), HttpCode.BadRequest

    tai_khoan = TaiKhoan(tai_khoan=tai_khoan, mat_khau=mat_khau, dien_thoai=dien_thoai)
    db.session.add(tai_khoan)
    db.session.commit()

    user = Users(tai_khoan_id = tai_khoan.id, dien_thoai=dien_thoai, ho=ho, ten=ten, email=email, vai_tro_id="6c167d69-c1d7-4beb-a023-57bc8fc95fbb")
    db.session.add(user)
    db.session.commit()

    return {
            "msg": "Tạo mới người dùng thành công", 
            # "nguoi_dung": schema.dump(user)
            }, HttpCode.Created






@blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {"access_token": access_token}
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    return jsonify(ret), HttpCode.OK


@blueprint.route("/revoke-access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), HttpCode.OK


@blueprint.route("/revoke-refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify({"message": "token revoked"}), HttpCode.OK


@blueprint.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    method_decorators = [jwt_required()]
    password = user_jwt.assigned_account.mat_khau
    old_password = request.json.get("old_password", None)
    new_password = request.json.get("new_password", None)
    retype_password = request.json.get("retype_password", None)

    if pwd_context.verify(old_password, password) is False:
        return (
            jsonify({"msg": "Enter a valid password and try again."}),
            HttpCode.BadRequest,
        )

    if new_password != retype_password:
        return jsonify({"msg": "Password do not match"}), HttpCode.BadRequest

    user = TaiKhoan.query.filter(TaiKhoan.id == user_jwt.tai_khoan_id).first()
    user.mat_khau = pwd_context.hash(new_password)
    db.session.commit()

    return jsonify({"msg": "Change Password Successfully"}), HttpCode.OK


@jwt.user_lookup_loader
def user_loader_callback(jwt_headers, jwt_payload):
    identity = jwt_payload["sub"]
    return Users.query.get(identity)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    if token_in_redis is not None:
        token_in_redis = json.loads(token_in_redis)
        return token_in_redis.get("revoked", False)
    return False


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=login, app=app)
    apispec.spec.path(view=refresh, app=app)
    apispec.spec.path(view=revoke_access_token, app=app)
    apispec.spec.path(view=revoke_refresh_token, app=app)
    apispec.spec.path(view=change_password, app=app)
