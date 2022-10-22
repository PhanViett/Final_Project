from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError
from application.models.lich_su_dao_tao import LichSuDaoTao
from application.models.user import User
from application.schemas.dao_tao import DaotaoSchema
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
from application.extensions import db
from application.commons.pagination import paginate

class DaoTaoResource(Resource):
    @jwt_required()
    def post(self):
        schema = DaotaoSchema()
        req = {
            "ma_chuong_trinh": request.form.get("ma_chuong_trinh"),
            "ten_chuong_trinh": request.form.get("ten_chuong_trinh"),
            "quy_doi_so_gio": request.form.get("quy_doi_so_gio"),
            "noi_dung_chuyen_mon": request.form.get('noi_dung_chuyen_mon'),
            "trang_thai": request.form.get('trang_thai'),
            "thoi_gian_duyet": request.form.get('thoi_gian_duyet'),
            "ten_truong": request.form.get('ten_truong'),
            "so_GCN_dao_tao": request.form.get('so_GCN_dao_tao'),
            "ngay_cap_GCN": request.form.get('ngay_cap_GCN'),
            "so_tiet_hoc": request.form.get('so_tiet_hoc')
        }
        try:
            dao_tao = schema.load(req)
            dao_tao.created_by = current_user.id
            if current_user.assigned_role[0].ten_en != "duocsi":
                dao_tao.nhan_vien_id = request.form.get('nhan_vien_id')
            else: 
                dao_tao.nhan_vien_id = current_user.id
            tu_ngay = request.form.get("tu_ngay")
            dao_tao.tu_ngay = tu_ngay
            den_ngay = request.form.get("den_ngay")
            dao_tao.den_ngay = den_ngay
            db.session.add(dao_tao)
            db.session.flush()
        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest
        
        chung_tu_dinh_kem = request.files.getlist('chung_tu_dinh_kem[]') if "chung_tu_dinh_kem[]" in request.files else None
        upload_errors = []
        chung_tu_dinh_kem = request.files.getlist('chung_tu_dinh_kem[]')
        if chung_tu_dinh_kem and len(chung_tu_dinh_kem) > 0:
            danh_sach_chung_tu_dk,errors = UploadMinio.upload_duocsi(chung_tu_dinh_kem, many=True)
            dao_tao.chung_tu_dinh_kem.extend(danh_sach_chung_tu_dk)
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_anh_chan_dung[]"):
            dao_tao.chung_tu_dinh_kem = [x for x in dao_tao.chung_tu_dinh_kem if x["url"] not in request.form.getlist("delete_dinh_kem_anh_chan_dung[]")]
            
        db.session.add(dao_tao)
        db.session.commit()
        return {"msg": "Tạo thành công", "results": schema.dump(dao_tao)}, HttpCode.Created
class DaoTaoById(Resource):

    @jwt_required()
    def put(self, id):

        schema = DaotaoSchema(partial =True)
        dao_tao = LichSuDaoTao.query.filter(LichSuDaoTao.id == id).first()
        if dao_tao is None:
            return {"errors": "No data"},  HttpCode.InternalError

        req = {
            "ma_chuong_trinh": request.form.get("ma_chuong_trinh"),
            "ten_chuong_trinh": request.form.get("ten_chuong_trinh"),
            "nhan_vien_id": current_user.id,
            "quy_doi_so_gio": request.form.get("quy_doi_so_gio"),
            "noi_dung_chuyen_mon": request.form.get('noi_dung_chuyen_mon'),
            "trang_thai": request.form.get('trang_thai'),
            "thoi_gian_duyet": request.form.get('thoi_gian_duyet'),
            "ten_truong": request.form.get('ten_truong'),
            "so_GCN_dao_tao": request.form.get('so_GCN_dao_tao'),
            "ngay_cap_GCN": request.form.get('ngay_cap_GCN'),
            "so_tiet_hoc": request.form.get('so_tiet_hoc')
        }
        try:
            dao_tao = schema.load(req, instance=dao_tao)
            dao_tao.updated_by = current_user.id
            dao_tao.updated_at = db.func.current_timestamp()
            dao_tao.nhan_vien_id = current_user.id
            tu_ngay = request.form.get("tu_ngay")
            dao_tao.tu_ngay = tu_ngay
            den_ngay = request.form.get("den_ngay")
            dao_tao.den_ngay = den_ngay
            db.session.add(dao_tao)
            db.session.flush()
        except ValidationError as err:
            return {"errors": err.messages},  HttpCode.BadRequest
        chung_tu_dinh_kem = request.files.getlist('chung_tu_dinh_kem[]') if "chung_tu_dinh_kem[]" in request.files else None
        upload_errors = []
        chung_tu_dinh_kem = request.files.getlist('chung_tu_dinh_kem[]')
        if chung_tu_dinh_kem and len(chung_tu_dinh_kem) > 0:
            danh_sach_chung_tu_dk,errors = UploadMinio.upload_duocsi(chung_tu_dinh_kem, many=True)
            dao_tao.chung_tu_dinh_kem.extend(danh_sach_chung_tu_dk)
            if errors:
                upload_errors.extend(errors)
        if request.form.get("delete_dinh_kem_anh_chan_dung[]"):
            dao_tao.chung_tu_dinh_kem = [x for x in dao_tao.chung_tu_dinh_kem if x["url"] not in request.form.getlist("delete_dinh_kem_anh_chan_dung[]")]
            
        db.session.commit()
        return {"msg": "Cập nhật thành công", "results": schema.dump(dao_tao)}, HttpCode.OK

    @jwt_required()
    def delete(self, id):

        schema = DaotaoSchema()
        dao_tao = LichSuDaoTao.query.filter(LichSuDaoTao.id == id).first()
        if dao_tao is None:
            return {"errors": "No data"},  HttpCode.InternalError
        db.session.delete(dao_tao)
        db.session.commit()

        return  {"msg": "Xóa thành công"}, HttpCode.OK
class DaoTaoGetList(Resource):
    @jwt_required()
    def post(self):
        schema = DaotaoSchema(many =True)
        id = request.json.get("nhan_vien_id") 
        query = LichSuDaoTao.query.filter(LichSuDaoTao.nhan_vien_id == id)
        return paginate(query, schema), HttpCode.OK
        
        # if data.get("search_ten"):
        #     search_ten = data["search_ten"]
        #     query = query.filter(GiayPhepKinhDoanh.ten_khong_dau.like(f"%{clean_string(search_ten)}%"))
            
              
        query = query.order_by(LichSuDaoTao.updated_at.desc()) 
        res = paginate(query,schema)
        if len(res["results"])  < 1:
            return {
                "msg":"Không có lịch sử đào tạo này!"
            }, HttpCode.OK
        
        return res, HttpCode.OK
    @jwt_required()
    def delete(self, id):

        schema = DaotaoSchema()
        dao_tao = LichSuDaoTao.query.filter(LichSuDaoTao.id == id).first()
        if dao_tao is None:
            return {"errors": "No data"},  HttpCode.InternalError
        db.session.delete(dao_tao)
        db.session.commit()

        return  {"msg": "Xóa thành công"}, HttpCode.OK
            
