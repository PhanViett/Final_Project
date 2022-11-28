import os
from flask import json
from flask_jwt_extended import (
    jwt_required
)
from flask import request, jsonify, Blueprint, current_app as app
from application.commons.pagination import paginate
from application.config import DEFAULT_USER_ID
from application.extensions import db, apispec
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from application.models import Users, VaiTro
from application.schemas.vai_tro import VaiTroSchema
import datetime
from application.utils.helper.role_helper import convert_to_permission, permissions_required
##########################################################################


blueprint = Blueprint("vai_tro", __name__, url_prefix="/api/v1/vai-tro")


@blueprint.route("/assign/<userid>/<roleid>", methods=["POST"])
@jwt_required()
@permissions_required("setting", ["manage_role"])
def assign_role(userid, roleid):

    # region Swagger UI
    """Assign nhan_vien with vai_tro
    ---
    post:
        tags:
          - vai_tro
        summary: Assign vai_tro
        description: Assign a nhan_vien with a vai_tro
        parameters:
          - in: path
            name: userid
            schema:
              type: string
          - in: path
            name: roleid
            schema:
              type: string
        responses:
          201:
            description: nhan_vien has been assigned successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    # CHECK IF userid OR role_id EXIST
    if not userid or not roleid:
        return {
            "errorCode": "EC07",
            "msg": "Thiếu id của người dùng hoặc của vai trò"
        }, HttpCode.BadRequest

    # CHECK IF USER EXISTS
    target_nhan_vien: NhanVien = NhanVien.query.filter_by(id=userid).first()
    target_vai_tro: VaiTro = VaiTro.query.filter_by(id=roleid).first()
    if not target_nhan_vien:
        return {
            "errorCode": "EC10",
            "msg": "Người dùng không tồn tại"
        }, HttpCode.BadRequest

    # CHECK IF OBJECT EXISTS
    if not target_vai_tro:
        return {
            "errorCode": "EC10",
            "msg": "Vai trò không tồn tại"
        }, HttpCode.BadRequest

    target_nhan_vien.vai_tro_id = target_vai_tro.id
    db.session.commit()
    return {
        "msg": "Thay đổi vai trò thành công",
        "content": {
            "nhan_vien": f"{target_nhan_vien.ho}  {target_nhan_vien.ten}",
            "vai_tro": target_vai_tro.ten
        }
    }, HttpCode.Created


@blueprint.route("/unassign/<userid>", methods=["DELETE"])
@jwt_required()
def unassign_role(userid):
    target_nhan_vien: Users = Users.query.filter(Users.id == userid).first_or_404()
    target_nhan_vien.vai_tro_id = DEFAULT_USER_ID
    db.session.commit()
    return "Tước vai trò thành công", HttpCode.OK


@blueprint.route("", methods=["POST"])
@jwt_required()
@permissions_required("setting", ["manage_role"])
def add_role():
    # region Swagger UI
    """Add vai_tro
    ---
    post:
        tags:
          - vai_tro
        summary: Add vai_tro
        description: Add a new vai_tro
        requestBody:
          content:
            application/json:
              schema:
                VaiTroSchema
        responses:
          201:
            description: VaiTro has been created successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    # CHECK IF REQUEST IS APPROPRIATE
    if "ten" not in request.json and not request.json["ten"]:
        return {"msg": "Thiếu tên vai trò"}, HttpCode.BadRequest

    # CHECK IF THE VaiTro IS ALREADY EXIST
    if VaiTro.query.filter(VaiTro.ten == request.json.get("ten", None)).first():
        return {"msg":"Vai trò đã tồn tại"}, HttpCode.BadRequest

    # SETUP SCHEMA AND TURN JSON INTO THE CORRECT OBJECT
    schema = VaiTroSchema()
    role: VaiTro = schema.load(request.json)
    temp = role.vai_tro
    role.vai_tro = json.dumps(convert_to_permission(json.loads(role.vai_tro)))

    # ADD DATA TO THE DATABASE AND COMMIT
    db.session.add(role)
    db.session.commit()
    role.vai_tro = temp
    return {
        "msg": "Tạo vai trò thành công",
        "content": schema.dump(role)
    }, HttpCode.Created


@ blueprint.route("/<id>", methods=["PUT"])
@jwt_required()
@permissions_required("setting", ["manage_role"])
def update_role(id):
    # region Swagger UI
    """Update vai_tro
    ---
    put:
        tags:
          - vai_tro
        summary: Update vai_tro
        description: Update a vai_tro with new data
        parameters:
          - in: path
            name: id
            schema:
              type: string
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  vai_tro:
                    type: string
                    required: true
                  ten:
                    type: string
                    example: name
                    required: true
        responses:
          200:
            description: VaiTro has been updated successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion
    # SETUP SCHEMA AND TURN JSON INTO THE CORRECT OBJECT
    role: VaiTro = VaiTro.query.get_or_404(id)
    if "vai_tro" in request.json:
        role.vai_tro = json.dumps(convert_to_permission(json.loads(request.json.get("vai_tro", None))))
    else:
        temp_vai_tro = role.vai_tro
    if "ten" in request.json:
        role.ten = request.json.get("ten", None)
    if "trang_thai" in request.json:
        role.trang_thai = request.json.get("trang_thai", None)
    db.session.commit()
    return {
        "msg": "Cập nhật vai trò thành công",
        "content": request.json
    }, HttpCode.OK


@ blueprint.route("/<id>", methods=["GET"])
@jwt_required()
@permissions_required("setting", ["manage_role"])
def get_role(id):
    # region Swagger UI
    """Get vai_tro
    ---
    get:
        tags:
          - vai_tro
        summary: Get a vai_tro
        description: Get a vai_tro via id
        parameters:
          - in: path
            name: id
            schema:
              type: string
        responses:
          200:
            content:
              application/json:
                schema:
                  VaiTroSchema
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    # CHECK IF id IS NOT EMPTY ELSE RETURN RESPONSE STATUS 400
    role: VaiTro = VaiTro.query.get_or_404(id)
    result_role = json.loads(role.vai_tro)
    for permission_category in result_role:
        permission_category["children"] = [
            permission for permission in permission_category["children"] if permission["checked"]]
    result_role = [category for category in result_role if len(category["children"])]
    role.vai_tro = json.dumps(result_role)
    return {
        "msg": "Thành công",
        "results": VaiTroSchema().dump(role)
    }, HttpCode.OK


@ blueprint.route("/get-list", methods=["POST"])
@jwt_required()
@permissions_required("setting", ["manage_role"])
def get_role_list():
    # region Swagger UI
    """Get list of roles
    ---
    post:
        tags:
          - vai_tro
        summary: Get list of roles
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  search_ten:
                      type: string
                  order_ten:
                      type: string
                  created_date:
                      type: string
                      enum: [asc,desc]
        description: Get a list of roles
        responses:
          200:
            description: success
            content:
              application/json:
                schema:
                  allOf:
                    - type: array
                      items:
                        $ref: '#/components/schemas/VaiTroSchema'
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion   print(roles)

    schema = VaiTroSchema(many=True, exclude=["vai_tro"])
    # GET LIST OF VaiTro
    query = VaiTro.query
    if not request.json:
        query = query.order_by(VaiTro.created_at.desc())
        return paginate(query, schema), HttpCode.OK
    if "order_ten" in request.json and request.json.get("order_ten"):
        order_ten = request.json.get("order_ten")
        if order_ten == "asc":
            query = query.order_by(VaiTro.ten.asc())
        elif order_ten == "desc":
            query = query.order_by(VaiTro.ten.desc())
    if "created_date" in request.json and request.json.get("created_date"):
        created_date = request.json.get("created_date")
        if created_date == "asc":
            query = query.order_by(VaiTro.created_at.asc())
        elif created_date == "desc":
            query = query.order_by(VaiTro.created_at.desc())
    if "search_ten" in request.json and request.json.get("search_ten"):
        ten_to_search = request.json.get("search_ten")
        query = query.filter(VaiTro.ten_en.like(f"%{clean_string(ten_to_search)}%"))
    return paginate(query, schema), HttpCode.OK


@ blueprint.route("/<userid>", methods=["GET"])
@jwt_required()
@permissions_required("setting", ["manage_role"])
def get_user_role(userid):
    # region Swagger UI
    """Get nhan_vien roles
    ---
    get:
        tags:
          - vai_tro
        summary: Get nhan_vien's roles
        description: Get roles of nhan_vien
        parameters:
          - in: path
            name: userid
            schema:
              type: string
        responses:
          200:
            description: bad request
            content:
              application/json:
                schema:
                  allOf:
                    - type: array
                      items:
                        VaiTroSchema
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion
    # GET THE ROLES USING THE userid
    schema = VaiTroSchema(many=True)
    nhan_vien: NhanVien = NhanVien.query.filter(NhanVien.id == userid).first_or_404()
    return {
        "msg": "Thna"
    }, HttpCode.OK


@ blueprint.route("/<id>", methods=["DELETE"])
@jwt_required()
@permissions_required("setting", ["manage_role"])
def delete_role(id):
    # region Swagger UI
    """Delete vai_tro
    ---
    delete:
        tags:
          - vai_tro
        summary: Delete a vai_tro
        description: Delete a vai_tro via id
        parameters:
          - in: path
            name: id
            schema:
              type: string
        responses:
          200:
            description: VaiTro has been deleted successfully
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion

    # GET THE ROLE USING PROVIDED id
    role: VaiTro = VaiTro.query.filter(VaiTro.id == id).first_or_404()
    # IF vai_tro HADN'T BEEN DELETED THEN SET TIMESTAMP
    if len(role.nhan_vien) > 0:
        return {
            "errorCode": "EC04",
            "msg": "Không thể xóa vai trò do có người dùng phụ thuộc"
        }, HttpCode.OK
    db.session.delete(role)
    db.session.commit()
    return {
        "msg": "Xóa vai trò thành công"
    }, HttpCode.OK


@ blueprint.route("/default-permission", methods=["GET"])
@jwt_required()
@permissions_required("setting", ["manage_role"])
def get_default_permission():
    # region Swagger UI
    """Get nhan_vien roles
    ---
    get:
        tags:
          - vai_tro
        summary: Get the default permission
        description: Get the default permission
        responses:
          200:
            description: return a permissions json
          400:
            description: bad request
          401:
            description: unauthorized
    """
    # endregion
    print(os.getcwd())
    test = open('application/permissions.json')
    test = json.load(test)
    return {
        "msg": "Thành công",
        "content": test
    }, HttpCode.OK


@ blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("VaiTroSchema", schema=VaiTroSchema)
    apispec.spec.path(view=assign_role, app=app)
    apispec.spec.path(view=add_role, app=app)
    apispec.spec.path(view=update_role, app=app)
    apispec.spec.path(view=get_role, app=app)
    apispec.spec.path(view=delete_role, app=app)
    apispec.spec.path(view=unassign_role, app=app)
    apispec.spec.path(view=get_role_list, app=app)
    apispec.spec.path(view=get_user_role, app=app)
    apispec.spec.path(view=get_default_permission, app=app)
