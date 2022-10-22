
from application.extensions import ma, db
from application.models.quan_huyen import QuanHuyen

class QuanHuyenSchema(ma.SQLAlchemyAutoSchema):
     id = ma.auto_field(dump_only=True)

     class Meta:
            model = QuanHuyen
            sqla_session = db.session
            load_instance = True
            exclude = ("created_at", "updated_at", "deleted_at")