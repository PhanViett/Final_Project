from flask import json
from marshmallow_sqlalchemy.schema import auto_field
from application.models import User
from application.extensions import ma, db
from marshmallow import validate, fields
from application.models import VaiTro


class VaiTroSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    # updated_at = ma.auto_field(dump_only=True)

    class Meta:
        model = VaiTro
        sqla_session = db.session
        load_instance = True
        exclude = ("created_by", "created_at", "deleted_at", "updated_at")


class VaiTroDisplaySchema(ma.SQLAlchemySchema):
    id = ma.auto_field(dump_only=True)
    ten_vai_tro = fields.String(attribute="ten")

    class Meta:
        model = VaiTro
        sqla_session = db.session
        load_instance = True


class VaiTroSelectBoxSchema(ma.SQLAlchemySchema):
    value = fields.String(attribute="id", dump_only=True)
    label = fields.String(attribute="ten", dump_only=True)

    class Meta:
        model = VaiTro
        sqla_session = db.session
        load_instance = True
