
from application.extensions import ma, db
from application.models.danhmuc_hoi_dong import HoiDong
class HoiDongSchema(ma.SQLAlchemyAutoSchema):
     id = ma.auto_field(dump_only=True)
    # is_super_admin = ma.auto_field(load_only=True)
     class Meta:
            model = HoiDong
            sqla_session = db.session
            load_instance = True
          #   exclude = ("created_at", "updated_at", "deleted_at")