
from application.extensions import ma, db
from application.models.danhmuc_thanh_phan_ho_so import ThanhPhanHoSo
from application.schemas.danhmuc_thu_tuc import DanhMucThuTucSchema
from marshmallow import fields

class ThanhPhanHoSoSchema(ma.SQLAlchemyAutoSchema):
     id = ma.auto_field(dump_only=True)
     thu_tuc = ma.Nested(DanhMucThuTucSchema)
     
     # ma_thu_tuc = ma.auto_field()
    # is_super_admin = ma.auto_field(load_only=True)
     class Meta:
          include_fk = True
          include_relationship = True  
          model = ThanhPhanHoSo
          sqla_session = db.session
          load_instance = True
          exclude = ("created_at", "updated_at", "deleted_at")