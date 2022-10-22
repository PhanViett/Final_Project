from application.extensions import ma, db
from application.models.bang_thong_bao import ThongBao
from marshmallow import fields


class ThongBaoSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)

    class Meta:
        model = ThongBao
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at")
