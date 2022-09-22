from application.minio_handler import MinioHandler
from io import BytesIO

config = {
    "bucket": "congsuckhoe",
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

    def upload_image_tin_tuc(file):
        data = file.read()
        file_name = " ".join(file.filename.strip().split())
        data_file = (
            MinioHandler()
            .get_instance()
            .save_image_tin_tuc(
                bucket=config.get("bucket"), file_name=file_name, file_data=BytesIO(data)
            )
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
        return data_file, file_name

    def remove_image(file_name):
        data_file = MinioHandler().get_instance().remove_picture_tin_tuc(
            bucket="congsuckhoe",
            file_name=file_name
        )
