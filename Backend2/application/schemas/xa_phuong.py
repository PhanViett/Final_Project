
from application.extensions import ma, db
from application.models.xa_phuong import XaPhuong

class XaPhuongSchema(ma.SQLAlchemyAutoSchema):
     id = ma.auto_field(dump_only=True)

     class Meta:
            model = XaPhuong
            sqla_session = db.session
            load_instance = True
            exclude = ("created_at", "updated_at", "deleted_at")