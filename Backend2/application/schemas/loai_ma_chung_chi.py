from application.extensions import ma, db
from marshmallow import fields
from application.models.loai_ma_chung_chi import LOAIMACHUNGCHI
class LoaiMaChungChichema(ma.SQLAlchemyAutoSchema):
     id = ma.auto_field(dump_only=True)
     class Meta:
            model = LOAIMACHUNGCHI
            sqla_session = db.session
            load_instance = True
          #   exclude = ("created_at", "updated_at", "deleted_at")
            exclude = ("created_at", "updated_at", "deleted_at", "deleted","created_by","updated_by","deleted_by")



