from sys import meta_path
from flask import json
from marshmallow.utils import EXCLUDE
from marshmallow_sqlalchemy.schema import auto_field
from application.models import NhanVien
from application.extensions import ma, db
from marshmallow import validate, fields
from application.models import VaiTro


class VaiTroSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)

    class Meta:
        model = VaiTro
        sqla_session = db.session
        load_instance = True
        exclude = ("created_by", "created_at", "deleted_at", "ten_en")
