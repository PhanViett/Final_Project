from marshmallow import fields
from application.extensions import ma, db
from application.models.danhmuc_pham_vi_hoat_dong_kinh_doanh import PhamViHoatDongKinhDoanh


class PhamVihoatDongKinhDoanhSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
   # is_super_admin = ma.auto_field(load_only=True)

    class Meta:
        model = PhamViHoatDongKinhDoanh
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")


class PhamViHoatDongKinhDoanhDisplaySchema(ma.SQLAlchemySchema):
    value = fields.String(attribute="id", dump_only=True)
    label = fields.String(attribute="ten", dump_only=True)

    class Meta:
        model = PhamViHoatDongKinhDoanh
        sqla_session = db.session
        load_instance = True


class PhamViHoatDongKinhDoanhParentDisplaySchema(ma.SQLAlchemySchema):
    id = fields.String(attribute="id", dump_only=True)
    ten = fields.String(attribute="ten", dump_only=True)
    value = fields.Nested(nested=PhamViHoatDongKinhDoanhDisplaySchema, attribute="children", many=True)

    class Meta:
        model = PhamViHoatDongKinhDoanh
        sqla_session = db.session
        load_instance = True
