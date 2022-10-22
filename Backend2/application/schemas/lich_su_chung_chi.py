from application.extensions import ma, db
from marshmallow import fields

from application.models.lich_su_chung_chi import LichSuChungChi

class LichSuChungChiSchema(ma.SQLAlchemyAutoSchema):
     id = ma.auto_field(dump_only=True)
     # ma_doi_tuong_id = ma.auto_field()
     # ten_doi_tuong_id = ma.auto_field()
     



     class Meta:
            model = LichSuChungChi
            include_fk = True
            # include_relationship = True
            sqla_session = db.session
            load_instance = True
            exclude = ("created_at", "updated_at", "deleted_at", "deleted","created_by","updated_by")