from application.models import VaiTro
from marshmallow.utils import EXCLUDE
from application.extensions import db, ma

from marshmallow_sqlalchemy.schema import auto_field


class VaiTroSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)

    class Meta:
        model = VaiTro
        sqla_session = db.session
        load_instance = True
        exclude = ("created_by", "created_at", "updated_at", "deleted_at")
