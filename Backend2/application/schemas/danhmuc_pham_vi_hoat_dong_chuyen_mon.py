
from application.extensions import ma, db
from marshmallow import fields
from application.models.danhmuc_pham_vi_hoat_dong_chuyen_mon import PhamViHoatDongChuyenMon
class PhamViHoatDongChuyenMonSchema(ma.SQLAlchemyAutoSchema):
     id = ma.auto_field(dump_only=True)
    # is_super_admin = ma.auto_field(load_only=True)
     class Meta:
            model = PhamViHoatDongChuyenMon
            sqla_session = db.session
            load_instance = True
            exclude = ("created_at", "updated_at", "deleted_at")

class PhamViHoatDongChuyenMonDisplaySchema(ma.SQLAlchemySchema):
     value= fields.String(attribute="id",dump_only=True)
     label= fields.String(attribute="ten", dump_only=True)
    # is_super_admin = ma.auto_field(load_only=True)
     class Meta:
            model = PhamViHoatDongChuyenMon
            sqla_session = db.session
            load_instance = True
