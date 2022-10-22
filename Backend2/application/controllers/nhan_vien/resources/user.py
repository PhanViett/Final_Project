from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from application.models.tai_khoan import TaiKhoan
from application.models.vai_tro import VaiTro
from application.utils.resource.http_code import HttpCode
from application.schemas import NhanVienSchema
from application.models import User
from application.extensions import db, pwd_context
from application.commons.pagination import paginate
from application.utils.validate.uuid_validator import is_valid_uuid


class UserResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - nhan_vien
      summary: Get a nhan_vien
      description: Get a single nhan_vien by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  nhan_vien: NhanVienSchema
        404:
          description: nhan_vien does not exists
    put:
      tags:
        - nhan_vien
      summary: Update a nhan_vien
      description: Update a single nhan_vien by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              NhanVienSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: nhan_vien updated
                  nhan_vien: NhanVienSchema
        404:
          description: nhan_vien does not exists
    delete:
      tags:
        - nhan_vien
      summary: Delete a nhan_vien
      description: Delete a single nhan_vien by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: nhan_vien deleted
        404:
          description: nhan_vien does not exists
    """

    method_decorators = [jwt_required()]

    def get(self, user_id):
        schema = NhanVienSchema()
        user: User = User.query.get_or_404(user_id)
        user_dict: dict = schema.dump(user)
        # user_dict.update({"ten_vai_tro": user.assigned_role.ten if user.assigned_role else None})
        return {"nhan_vien": user_dict}, HttpCode.OK

    def put(self, user_id):
        schema = NhanVienSchema(partial=True)
        user: User = User.query.get_or_404(user_id)
        new_user_info = {}
        for key in request.json.keys():
            if request.json[key] or request.json[key] == False:
                new_user_info[key] = request.json[key]
        if "mat_khau" in new_user_info:
            mat_khau = pwd_context.hash(new_user_info["mat_khau"])
            del new_user_info["mat_khau"]
            target_tai_khoan: TaiKhoan = TaiKhoan.query.filter(TaiKhoan.id == user.tai_khoan_id).first()
            if target_tai_khoan:
                target_tai_khoan.mat_khau = pwd_context.hash(mat_khau)

        user:User = schema.load(new_user_info, instance=user)

        db.session.commit()

        return {"msg": "nhan_vien updated", "nhan_vien": schema.dump(user)}, HttpCode.OK

    def delete(self, user_id):
        user: User = User.query.get_or_404(user_id)
        tai_khoan = TaiKhoan.query.filter(TaiKhoan.id == user.tai_khoan_id).first_or_404()
        db.session.delete(user)
        db.session.delete(tai_khoan)
        db.session.commit()

        return {"msg": "nhan_vien deleted"}, HttpCode.OK


class UserList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - nhan_vien
      summary: Get a list of users
      description: Get a list of paginated users
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/NhanVienSchema'
    post:
      tags:
        - nhan_vien
      summary: Create a nhan_vien
      description: Create a new nhan_vien
      requestBody:
        content:
          application/json:
            schema:
              NhanVienForSwaggerSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: nhan_vien created
                  nhan_vien: NhanVienForSwaggerSchema
    """

    method_decorators = [jwt_required()]

    def get(self):
        schema = NhanVienSchema(many=True)
        query = User.query
        return paginate(query, schema)

    def post(self):
        # if not "vai_tro_id" in request.json and not request.json["vai_tro_id"]:
        #     request.json["vai_tro_id"] = "bdb5aa16-1cc0-4cce-bd63-bd5069ec346a"
        if not "tai_khoan" in request.json and not request.json["tai_khoan"]:
            return{
                "errorCode": "EC01",
                "msg": "Thiếu tên tài khoản! vui lòng nhập tài khoản"
            }, HttpCode.BadRequest
        if not "mat_khau" in request.json and not request.json["mat_khau"]:
            return{
                "errorCode": "EC01",
                "msg": "Thiếu mật khẩu! vui lòng nhập mật khẩu"
            }, HttpCode.BadRequest
        if TaiKhoan.query.filter(TaiKhoan.tai_khoan == request.json["tai_khoan"]).first():
            return{
                "errorCode": "EC03",
                "msg": "Tên tài khoản đã tồn tại"
            }, HttpCode.BadRequest
        ten_tai_khoan = request.json["tai_khoan"]
        mat_khau = request.json["mat_khau"]
        del request.json["tai_khoan"]
        del request.json["mat_khau"]
        tai_khoan = TaiKhoan(tai_khoan=ten_tai_khoan, mat_khau=mat_khau)
        db.session.add(tai_khoan)
        request.json["tai_khoan_id"] = str(tai_khoan.id)

        schema = NhanVienSchema()
        user: User = schema.load(request.json)
        db.session.add(user)
        db.session.commit()
        return {"msg": "Tạo tài khoản thành công", "nhan_vien": schema.dump(user)}, HttpCode.Created


class UserInform(Resource):

    """Single object resource

   ---
   get:
     tags:
       - nhan_vien
     summary: Automatic User loading
     description: Get a nhan_vien by jwt login
     responses:
       200:
         content:
           application/json:
             schema:
               type: object
               properties:
                 nhan_vien: NhanVienSchema
       404:
         description: nhan_vien does not exists
   """
    @ jwt_required()
    def get(self):

        method_decorators = [jwt_required()]

        return jsonify(
            id=current_user.id,
            email=current_user.email,
            last_name=current_user.last_name,
            first_name=current_user.first_name,
            address=current_user.address,
            phone=current_user.phone,
        )


class UserSearch(Resource):

    """Single object resource

      ---
      get:
        tags:
          - nhan_vien
        summary: Search User by First Name
        description: Search nhan_vien get list
        parameters:
          - in: query
            name: search_key
            schema:
              type: string
        responses:
          200:
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    nhan_vien: NhanVienSchema
          404:
            description: nhan_vien does not exists
      """

    method_decorators = [jwt_required()]

    def get(self):
        search_key = request.args.get('search_key')
        schema = NhanVienSchema(many=True)
        query = User.query.filter(User.first_name.match(search_key) | User.phone.match(search_key))
        return paginate(query, schema)
    
    
    
class UserAssignRole(Resource):
    def put(self, user_id):
          if not is_valid_uuid(user_id):
              return {
                    "msg":"ID sai định dạng"
                },HttpCode.BadRequest        
          if not request.json.get("vai_tro_id", None):
                return {
                    "msg":"Thieu vai_tro_id"
                },HttpCode.BadRequest  
          target_role = VaiTro.query.get(request.json["vai_tro_id"])
          if not target_role:
                return {
                      "msg": "Vai tro khong ton tai"
                  }, HttpCode.BadRequest
          user = User.query.get_or_404(user_id)
          user.assigned_role.append(target_role)
          db.session.commit()
          return {
            "msg":"Thanh cong"
          }, HttpCode.OK
          
class UserUnassignRole(Resource):
    def put(self, user_id):
          if not is_valid_uuid(user_id):
              return {
                    "msg":"ID sai định dạng"
                },HttpCode.BadRequest        
          if not request.json.get("vai_tro_id", None):
                return {
                    "msg":"Thieu vai_tro_id"
                },HttpCode.BadRequest  
          target_role = VaiTro.query.get(request.json["vai_tro_id"])
          if not target_role:
                return {
                      "msg": "Vai tro khong ton tai"
                  }, HttpCode.BadRequest
          user = User.query.get_or_404(user_id)
          user.assigned_role.remove(target_role)
          db.session.commit()
          return {
            "msg":"Thanh cong"
          }, HttpCode.OK