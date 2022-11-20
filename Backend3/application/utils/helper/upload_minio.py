import os
from io import BytesIO
from application.minio_handler import MinioHandler
from application.utils.resource.http_code import HttpCode

config = {
    "bucket": os.getenv("MINIO_BUCKET_NAME"),
}


class UploadMinio:

    def get_path(name):
        path_default = "/uploads/"
        switcher = {
            "tin_tuc": path_default+"tin_tuc",
            "import_don_vi": path_default+"imports/don-vi/",
        }
        return switcher.get(name, path_default)


    def upload_image_tin_tuc(file, many=False):
        if many:
            if not isinstance(file, list):
                return {"msg": "Loại file không phải là một danh sách"}, HttpCode.BadRequest
            url_list = []
            error_messages = []
            for target in file:
                try:
                    if not target.content_type:
                        raise Exception()
                    data = target.read()
                    file_name = " ".join(target.filename.strip().split())
                    data_file = MinioHandler().get_instance().save_image_tin_tuc(bucket=config.get("bucket"), file_name=file_name, file_data=BytesIO(data))
                    # data_file = MinioHandler().save_image_tin_tuc(bucket=config.get("bucket"), file_name=file_name, file_data=BytesIO(data))
                    url_list.append({"name": file_name, "url": data_file})
                except Exception as e:
                    error_messages.append(target.filename+" tải lên thất bại")
            return url_list, error_messages
        data = file.read()
        file_name = " ".join(file.filename.strip().split())
        data_file = MinioHandler().get_instance().save_image_tin_tuc(bucket=config.get("bucket"), file_name=file_name, file_data=BytesIO(data))
        return data_file



    def remove_image(file_name):
        data_file = MinioHandler().get_instance().remove_picture_tin_tuc(
            bucket="congsuckhoe",
            file_name=file_name
        )
