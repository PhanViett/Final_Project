
from application.extensions import ma, db
from application.models.tinh_thanh import TinhThanh
from marshmallow import fields


class TinhThanhSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)

    class Meta:
        model = TinhThanh
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")


class TinhThanhDisplayCMNDSchema(ma.SQLAlchemySchema):
    value = fields.String(attribute="id", dump_only=True)
    label = fields.Method("set_label")

    class Meta:
        model = TinhThanh
        sqla_session = db.session
        load_instance = True

    def set_label(self, obj: TinhThanh):
        if obj.active == "1" and not obj.loai == 1:
            obj.ten = 'CA'+" "+obj.ten
        return obj.ten
