from marshmallow import fields
from application.extensions import ma, db
from application.models.record import Records


class RecordSchema(ma.SQLAlchemySchema):
    id = ma.auto_field(dump_only=True)
    user_id = ma.auto_field()
    ho_ten = fields.String(attribute="users.ho_ten")
    tuoi = ma.auto_field()
    gioi_tinh = ma.auto_field()
    height = ma.auto_field()
    weight = ma.auto_field()
    ap_hi = ma.auto_field()
    ap_lo = ma.auto_field()
    chol = ma.auto_field()
    gluc = ma.auto_field()
    smoke = ma.auto_field()
    alco = ma.auto_field()
    active = ma.auto_field()
    result = ma.auto_field()

    class Meta:
        model = Records
        sqla_session = db.session
        load_instance = True

