import io
from mimetypes import guess_extension
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from application.utils.helper.upload_minio import UploadMinio
from application.utils.resource.http_code import HttpCode
import requests


class InHoSo(Resource):
    @jwt_required()
    def post(self):
        url = request.json.get("url")
        file_name = request.json.get("file_name")
        file_type = request.json.get("file_type")
        if file_name is None or file_name == "":
            return {"msg": "Không xác đinh được tên file"}

        if url is None or url == "":
            return {"msg": "Không xác đinh được url"}

        if not file_type:
            return {"msg": "Không xác đinh được định dạng file"}
        try:
            if request.args.get("many", False):
                body = {"ids": request.json.get("ids"), "ten_chuc_vu": request.json.get("ten_chuc_vu"), "ten_nguoi_ky": request.json.get("ten_nguoi_ky")}
                response = requests.post(url, json=body)
            else:
                response = requests.get(url)
            if response.status_code != 200:
                return {
                    "msg": "Thông thể nhận được file"
                }, HttpCode.BadRequest
        except ConnectionError as e:
            print("Không thể kết nối tới server chứa tệp tin")
            return False
        if "content-type" in response.headers:
            file_extension = guess_extension(response.headers['content-type'].partition(';')[0].strip())
        else :
            file_extension = ".pdf"
        file_stream = io.BytesIO(response.content)
        path = UploadMinio.upload_ho_so_in(file=file_stream, file_name=file_name+file_extension, file_type=file_type)
        return {"msg": "OK", "path": path}, HttpCode.OK
