from datetime import timedelta
from application.minio_handler import MinioHandler
from io import BytesIO

from application.utils.resource.http_code import HttpCode

config = {
    "bucket": "cchnd",
}


class UploadMinio:

    def get_path(name):
        path_default = "/uploads/"
        switcher = {
            "tin_tuc": path_default+"tin_tuc",
            "import_don_vi": path_default+"imports/don-vi/",
        }
        return switcher.get(name, path_default)

    def upload_common(file, path):
        data = file.read()
        file_name = " ".join(file.filename.strip().split())
        data_file = (
            MinioHandler()
            .get_instance()
            .save_file_path(
                file_data=BytesIO(data), file_name=file_name, path=path
            )
        )
        return data_file

    def upload_duocsi(file, many=False):
        if many:
            if not isinstance(file, list):
                return {
                    "msg": "Loại file phải là một danh sách"
                }, HttpCode.BadRequest
            url_list = []
            error_messages = []
            for target in file:
                try:
                    if not target.content_type:
                        raise Exception()
                    data = target.read()
                    file_name = " ".join(target.filename.strip().split())
                    data_file = (
                        MinioHandler()
                        .get_instance()
                        .save_duocsi_files(
                            bucket=config.get("bucket"), file_name=file_name, file_data=BytesIO(data)
                        )
                    )
                    url_list.append({"name": file_name, "url": data_file})
                except Exception as e:
                    error_messages.append(target.filename+" tải lên thất bại")
            return url_list, error_messages
        data = file.read()
        file_name = " ".join(file.filename.strip().split())
        data_file = MinioHandler()\
            .get_instance()\
            .save_duocsi_files(
                bucket=config.get("bucket"), file_name=file_name, file_data=BytesIO(data)
        )
        return data_file

    def upload_files_van_ban(file):
        data = file.read()
        file_name = " ".join(file.filename.strip().split())
        data_file = (
            MinioHandler()
            .get_instance()
            .save_image_van_ban(
                bucket=config.get("bucket"), file_name=file_name, file_data=BytesIO(data)
            )
        )
        return data_file

    def remove_image(file_name):
        data_file = MinioHandler().get_instance().remove_picture_tin_tuc(
            bucket="congsuckhoe",
            file_name=file_name
        )

    def upload_ho_so_in(file: BytesIO, file_name: str, file_type: str):
        minio = MinioHandler().get_instance()
        data_file = (
            minio.save_default_file_path(
                file_name=file_name, file_data=file, path="/ho_so_in/"+file_type+"/")
        )
        url = minio.presigned_get_object(
            bucket_name=minio.bucket_name["bucket"], object_name="ho_so_in/"+file_type+"/"+file_name),
        return url
