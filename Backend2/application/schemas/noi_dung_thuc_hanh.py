
from application.extensions import ma, db
from application.models.noi_dung_thuc_hanh import NoiDungThucHanh

class NoiDungThucHanhSchema(ma.SQLAlchemyAutoSchema):
     id = ma.auto_field(dump_only=True)

     class Meta:
            model = NoiDungThucHanh
            sqla_session = db.session
            load_instance = True
            exclude = ("created_at", "updated_at", "deleted_at","created_by","deleted_by","deleted","updated_by")