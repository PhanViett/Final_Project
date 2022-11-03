import random
from datetime import datetime, timedelta
from sys import prefix
from urllib import response
import os
from flask import jsonify
from minio import Minio
from application.commons.progress import Progress

config = {"bucket": "congsuckhoe"}


class MinioHandler:
    __instance = None

    @staticmethod
    def get_instance():
        """Static access method."""
        if not MinioHandler.__instance:
            MinioHandler.__instance = MinioHandler()
        return MinioHandler.__instance

    def __init__(self):
        self.minio_url = os.getenv("MINIO_URL")
        self.access_key = os.getenv("MINIO_ACCESS_KEY")
        self.secret_key = os.getenv("MINIO_SECRET_KEY")
        self.bucket_name = {"bucket": os.getenv("MINIO_BUCKET_NAME")}
        self.client = Minio(
            self.minio_url,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False,
        )
        self.make_bucket()

    def get_path(name):
        path_default = "/uploads/"
        switcher = {
            "tin_tuc": path_default + "tin_tuc",
            "default-excel": path_default + "file_mau/",
            "import_don_vi": path_default + "imports/don-vi/",
            "import_ncnc": path_default + "imports/nhom-co-nguy-co-cao/",
            "import_ho_so_dieu_tri": path_default + "imports/ho-so-dieu-tri/",
            "import_ho_so_nnc": path_default + "imports/ho-so-nhom-nguy-co/",
            "import_ho_so_tiem_chung": path_default + "imports/ho-so-tiem-chung/",
            "import_ho_so_cap_do_dich": path_default + "imports/ho-so-cap-do-dich/",
            "import_ho_so_mac_benh": path_default + "imports/ho-so-mac-benh",
            "import_tctt": path_default + "imports/tiem-chung-theo-tuoi/",
            "slider_item_image": path_default + "slider/"
        }
        return switcher.get(name, path_default)

    def make_bucket(self):
        for bucket_name in self.bucket_name:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)

    def presigned_get_object(self, bucket_name, object_name):
        # Request URL expired after 7 days
        url = self.client.presigned_get_object(
            bucket_name=bucket_name, object_name=object_name, expires=timedelta(days=7)
        )
        return url

    def check_file_name_exists(self, bucket_name, file_name):
        try:
            self.client.stat_object(bucket_name=bucket_name, object_name=file_name)
            return True
        except Exception as e:
            print(f"[x] Exception: {e}")
            return False

    def save_image(self, bucket, file_data, file_name):
        try:
            datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            object_name = f"{datetime_prefix}___{file_name}"
            while self.check_file_name_exists(
                bucket_name=bucket, file_name=object_name
            ):
                random_prefix = random.randint(1, 1000)
                object_name = f"{datetime_prefix}___{random_prefix}___{file_name}"

            self.client.put_object(
                bucket_name=bucket,
                object_name="uploads/" + "images/" + object_name,  # Path + Name.ext
                data=file_data,
                length=-1,
                part_size=10 * 1024 * 1024,
            )

            return bucket + "/uploads" + "/images" + "/" + object_name

        except Exception as e:
            raise Exception(e)

    def save_image_tin_tuc(self, bucket, file_data, file_name):
        try:
            datetime_prefix = datetime.now().strftime("%H%M%S")
            object_name = f"{datetime_prefix}_{file_name}"
            while self.check_file_name_exists(
                bucket_name=bucket, file_name=object_name
            ):
                random_prefix = random.randint(1, 10000)
                object_name = f"{datetime_prefix}_{random_prefix}_{file_name}"

            self.client.put_object(
                bucket_name=bucket,
                object_name="uploads/" + "tin_tuc/" + object_name,  # Path + Name.ext
                data=file_data,
                length=-1,
                part_size=10 * 1024 * 1024,
            )

            return bucket + "/uploads" + "/tin_tuc" + "/" + object_name

        except Exception as e:
            raise Exception(e)

    def save_image_van_ban(self, bucket, file_data, file_name):
        try:
            datetime_prefix = datetime.now().strftime("%H%M%S")
            object_name = f"{datetime_prefix}_{file_name}"
            while self.check_file_name_exists(
                bucket_name=bucket, file_name=object_name
            ):
                random_prefix = random.randint(1, 100000)
                object_name = f"{datetime_prefix}_{random_prefix}_{file_name}"

            self.client.put_object(
                bucket_name=bucket,
                object_name="uploads/" + "van_ban/" + object_name,  # Path + Name.ext
                data=file_data,
                length=-1,
                part_size=10 * 1024 * 1024,
            )

            return bucket + "/uploads" + "/van_ban" + "/" + object_name

        except Exception as e:
            raise Exception(e)

    def remove_image(self, bucket, file_name):
        removed_bucket_path = file_name.replace(bucket + "/", "")
        try:
            self.client.remove_object(
                bucket_name=bucket, object_name=removed_bucket_path
            )
        except Exception as e:
            raise Exception(e)

    def remove_picture_tin_tuc(self, bucket, file_name):
        removed_bucket_path = file_name.replace(bucket + "/", "")
        try:
            self.client.remove_object(
                bucket_name=bucket, object_name=removed_bucket_path
            )
        except Exception as e:
            raise Exception(e)

    def put_object(self, file_data, file_name, content_type):
        try:
            datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            object_name = f"{datetime_prefix}___{file_name}"
            while self.check_file_name_exists(
                bucket_name=self.bucket_name, file_name=object_name
            ):
                random_prefix = random.randint(1, 1000)
                object_name = f"{datetime_prefix}___{random_prefix}___{file_name}"

            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,  # Path + Name.ext
                data=file_data,
                content_type=content_type,
                length=-1,
                part_size=10 * 1024 * 1024,
            )
            url = self.presigned_get_object(
                bucket_name=self.bucket_name, object_name=object_name
            )
            data_file = {
                "bucket_name": self.bucket_name,
                "file_name": object_name,
                "url": url,
            }
            return data_file
        except Exception as e:
            raise Exception(e)

    def save_file_path(self, file_data, file_name, path="/uploads/imports/", length=-1):
        bucket = config.get("bucket")
        try:
            datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            ten_file = f"{datetime_prefix}___{file_name}"
            while self.check_file_name_exists(bucket_name=bucket, file_name=ten_file):
                random_prefix = random.randint(1, 1000)
                ten_file = f"{datetime_prefix}___{random_prefix}___{file_name}"

            result = self.client.put_object(
                bucket_name=bucket,
                object_name=path + ten_file,  # Path + Name.ext
                data=file_data,
                length=length,
                part_size=10 * 1024 * 1024,
                progress=Progress(),
            )

            return result.bucket_name + result.object_name

        except Exception as e:
            raise Exception(e)

    def save_default_file_path(self, file_data, file_name, path="/uploads/imports/", length=-1):
        bucket = config.get("bucket")
        try:
            result = self.client.put_object(
                bucket_name=bucket,
                object_name=path + file_name,  # Path + Name.ext
                data=file_data,
                length=length,
                part_size=10 * 1024 * 1024,
            )

            return result.bucket_name + result.object_name

        except Exception as e:
            raise Exception(e)
