
from marshmallow import fields
from application.extensions import ma, db
from application.models.lich_su_dao_tao import LichSuDaoTao

class DaotaoSchema(ma.SQLAlchemyAutoSchema):
     id = ma.auto_field(dump_only=True)
     nguoi_duyet = fields.String(attribute="nhan_vien.ten")

     class Meta:
            model = LichSuDaoTao
            include_fk = True
            include_relationship = True
            sqla_session = db.session
            load_instance = True
            exclude = ("created_at", "updated_at", "deleted_at", "deleted","created_by","updated_by","deleted_by")
