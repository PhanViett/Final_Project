from marshmallow import fields
from application.extensions import ma, db
from application.models.danhmuc_van_bang_chuyen_mon import VanBangChuyenMon
class VanBangChuyenMonSchema(ma.SQLAlchemyAutoSchema):
     id = ma.auto_field(dump_only=True)
    # is_super_admin = ma.auto_field(load_only=True)
     class Meta:
            model = VanBangChuyenMon
            sqla_session = db.session
            load_instance = True
            exclude = ("created_at", "updated_at", "deleted_at")

class VanBangChuyenMonDisplaySchema(ma.SQLAlchemySchema):
     value = fields.String(attribute="id",dump_only=True)
     label = fields.String(attribute="ten", dump_only=True)
     
     class Meta:
            model = VanBangChuyenMon
            sqla_session = db.session
            load_instance = True
