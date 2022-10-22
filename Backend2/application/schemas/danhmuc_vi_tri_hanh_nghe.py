
from application.extensions import ma, db
from application.models.danhmuc_vi_tri_hanh_nghe import ViTriHanhNghe
from marshmallow import fields


class ViTriHanhNgheSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
   # is_super_admin = ma.auto_field(load_only=True)

    class Meta:
        model = ViTriHanhNghe
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at", "ten_khong_dau")


class ViTriHanhNgheDisplaySchema(ma.SQLAlchemySchema):
    value = fields.String(attribute="id", dump_only=True)
    label = fields.String(attribute="ten", dump_only=True)

    class Meta:
        model = ViTriHanhNghe
        sqla_session = db.session
        load_instance = True


class ViTriHanhNgheParentDisplaySchema(ma.SQLAlchemySchema):
    id = fields.String(attribute="id", dump_only=True)
    ten = fields.String(attribute="ten", dump_only=True)
    value = fields.Nested(nested=ViTriHanhNgheDisplaySchema, attribute="children",
                          dump_default=[], allow_none=True, many=True)

    class Meta:
        model = ViTriHanhNghe
        sqla_session = db.session
        load_instance = True
