from application.extensions import ma, db
from application.models.tin_tuc import TinTuc


class TinTucSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    title = ma.auto_field()
    content = ma.auto_field()
    status = ma.auto_field()
    user_id = ma.auto_field()
    
    class Meta:
        model = TinTuc
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "deleted_at", "deleted_by", "deleted")

