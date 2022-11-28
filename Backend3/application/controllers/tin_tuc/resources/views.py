from flask_restful import Resource
from flask import jsonify, request
from application.extensions import db
from application.models.tin_tuc import TinTuc
from application.models.nhan_vien import Users
from application.commons.pagination import paginate
from application.schemas.tin_tuc import TinTucSchema
from application.utils.resource.http_code import HttpCode
from flask_jwt_extended import jwt_required, current_user


class TinTucGetList(Resource):
    @ jwt_required()
    def post(self):
        schema = TinTucSchema(many=True)
        query = TinTuc.query.filter()
        data = request.json
        
        if not data:
            query = query.order_by(TinTuc.created_at.desc())
            return paginate(query, schema), HttpCode.OK

        if data.get("tieu_de"):
            tieu_de = data["tieu_de"]
            query = query.filter(TinTuc.title.like(f"%{tieu_de}%"))

        if data.get("status"):
            status = data["status"]
            query = query.filter(TinTuc.status == status)

        if data.get("user_id"):
            user_id = data["user_id"]
            query = query.filter(TinTuc.user_id == user_id)

        query = query.order_by(TinTuc.created_at.desc())
        res = paginate(query, schema)

        if len(res["results"]) > 0:
            for x in res["results"]:

                data = Users.query.filter(Users.id == x["user_id"]).first()
                if data is not None:
                    x["ho_ten"] = data.ho_ten

        return res, HttpCode.OK

class TinTucGetListView(Resource):
    @jwt_required()
    def post(self):
        schema_single = TinTucSchema()
        schema_many = TinTucSchema(many=True)

        blog_most = TinTuc.query.order_by(TinTuc.views.desc(), TinTuc.status != 3).first()
        blog_remain = TinTuc.query.filter(TinTuc.id != blog_most.id, TinTuc.status != 3).order_by(TinTuc.updated_at.desc()).all()
        
        return ({
            "status": "SUCCESS", 
            "most": schema_single.dump(blog_most), 
            "remain": schema_many.dump(blog_remain)
            }), HttpCode.OK

class TinTucDetail(Resource):
    @jwt_required()
    def post(self):
        schema = TinTucSchema()

        tin_tuc = TinTuc.query.filter(TinTuc.id == request.json.get("id")).first()

        if tin_tuc is None:
            return ({"status": "FAILED", "msg": "Bài viết không tồn tại trong hệ thống"}), HttpCode.BadRequest
        
        # if tin_tuc is not None and current_user.assigned_role[0].ten_en == "user":
        #     return ({"status": "FAILED", "msg": "Bạn không có quyền truy cập bài viết này"}), HttpCode.BadRequest

        tin_tuc.views = tin_tuc.views + 1
        
        db.session.commit()

        return jsonify({"status": "SUCCESS", "results": schema.dump(tin_tuc)})


class TinTucCreate(Resource):
    @jwt_required()
    def post(self):
        schema = TinTucSchema()

        req = {
            "title": request.json.get("title"),
            "content": request.json.get("content"),
            "status": 1,
        }

        tin_tuc = TinTuc( title=req["title"], content=req["content"], status=req["status"])
        
        tin_tuc.user_id = current_user.id

        db.session.add(tin_tuc)
        db.session.commit()
        
        return jsonify({"status": "SUCCESS", "msg": "Cập nhật bài viết thành công", "results": schema.dump(tin_tuc)})


class TinTucUpdate(Resource):
    @jwt_required()
    def put(self, id):
        schema = TinTucSchema()

        blog = TinTuc.query.filter(TinTuc.id == id).first()

        if not blog:
            return {"status": "FAILED", "msg": "Không tìm thấy bài viết"}, HttpCode.BadRequest
        elif blog.status == 3 and current_user.vai_tro["ten_en"] == "user":
            return {"status": "FAILED", "msg": "Bài viết không được chỉnh sửa sau khi đã xuất bản"}, HttpCode.BadRequest

        req = {
            "title": request.json.get("title"),
            "content": request.json.get("content"),
            "status": request.json.get("status")
        }

        blog = schema.load(req, instance=blog)

        db.session.commit()

        return {"status": "SUCCESS", "msg": "Cập nhật bài viết thành công", "results": schema.dump(blog)}, HttpCode.OK


class TinTucDelete(Resource):
    def delete(self, id):
        tin_tuc = TinTuc.query.filter(TinTuc.id == id).first()

        if tin_tuc is None:
            return jsonify({"status": "FAILED", "msg": "Bài viết không tồn tại trong hệ thống"}), HttpCode.BadRequest
        
        db.session.delete(tin_tuc)
        db.session.commit()

        return {"msg": "Xóa thông tin bài viết thành công!"}, HttpCode.OK
