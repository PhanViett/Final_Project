from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    current_user as user_jwt,
)
from application.models.tai_khoan import TaiKhoan
from application.models.vai_tro import VaiTro
from application.utils.helper.role_helper import get_user_permissions
from application.utils.resource.http_code import HttpCode
from application.schemas.nhan_vien import NhanVienSchema

from application.models import NhanVien
from application.extensions import pwd_context, jwt, apispec, db
from application.controllers.auth.helpers import (
    revoke_token,
    is_token_revoked,
    add_token_to_database,
)
import redis
from datetime import datetime, timedelta
import os
import json

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
    """Authenticate nhan_vien and return tokens
    ---
    post:
      tags:
        - auth
      summary: Authenticate a nhan_vien
      description: Authenticates a nhan_vien's credentials and returns tokens
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: admin
                  required: true
                password:
                  type: string
                  example: admin
                  required: true

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
                  refresh_token:
                    type: string
                    example: myrefreshtoken
        400:
          description: bad request
      security: []
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), HttpCode.BadRequest

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return (
            jsonify({"errorCode": "EC01", "msg": "Missing username or password"}),
            HttpCode.BadRequest,
        )

    # VALIDATE tai_khoan
    tai_khoan: TaiKhoan = TaiKhoan.query.filter_by(tai_khoan=username).first()
    if tai_khoan is None or not pwd_context.verify(password, tai_khoan.mat_khau):
        return (
            jsonify(
                {"errorCode": "EC01", "msg": "Username hoặc mật khẩu không chính xác"}
            ),
            HttpCode.BadRequest,
        )
    # SET LAST LOGIN FOR tai_khoan
    tai_khoan.last_login_at = datetime.now()
    
    # QUERY nhan_vien
    nhan_vien = NhanVien.query.filter(NhanVien.tai_khoan_id == tai_khoan.id).first()

    # APPLY TOKEN
    access_token = create_access_token(identity=nhan_vien.id)
    refresh_token = create_refresh_token(identity=nhan_vien.id)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

    user_data: dict = NhanVienSchema().dump(nhan_vien)

    # RETURN USER's ROLE
    vai_tro: VaiTro = nhan_vien.assigned_role
    if vai_tro:
        user_data.update({"ten_vai_tro": nhan_vien.assigned_role.ten})
    else:
        user_data.update({"ten_vai_tro": None})

    db.session.commit()
    ret = {
        "msg": "Đăng nhập thành công",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "userInfo": user_data,
        "permissions": get_user_permissions(nhan_vien)
    }

    return ret, HttpCode.OK


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
    revoke_token(jti, user_identity)
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
        description: Change password for nhan_vien
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
    return NhanVien.query.get(identity)


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
