from application.extensions import ma, db
from application.models.co_so_thuc_hanh import CoSoThucHanh
from marshmallow import ValidationError, fields, validates


class CoSoThucHanhSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    tinh_thanh = fields.Str(attribute="tinh_thanh.ten",allow_none=True,dump_default=None)
    xa_phuong =  fields.Str(attribute="xa_phuong.ten",allow_none=True,dump_default=None)
    quan_huyen =  fields.Str(attribute="quan_huyen.ten",allow_none=True,dump_default=None)
    class Meta:
        model = CoSoThucHanh
        include_fk = True
        include_relationship = True
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at", "deleted","created_by","updated_by")
class CoSoThucHanhDisPlaySchema(ma.SQLAlchemySchema):
    id = fields.String(dump_only=True)
   

    class Meta:
        model = CoSoThucHanh
        include_fk = True
        include_relationship = True
        sqla_session = db.session
        load_instance = True