from marshmallow import fields
from application.extensions import ma, db
from application.models.record import Records


class RecordSchema(ma.SQLAlchemySchema):
    id = fields.String(dump_only=True)
    ho_ten = fields.String(attribute="users.ho_ten", dump_only=True)
    tuoi = fields.String(dump_only=True)
    gioi_tinh = fields.String(dump_only=True)
    height = fields.String(dump_only=True)
    weight = fields.String(dump_only=True)
    ap_hi = fields.String(dump_only=True)
    ap_lo = fields.String(dump_only=True)
    chol = fields.String(dump_only=True)
    gluc = fields.String(dump_only=True)
    smoke = fields.String(dump_only=True)
    alco = fields.String(dump_only=True)
    active = fields.String(dump_only=True)
    result = fields.String(dump_only=True)

    class Meta:
        model = Records
        sqla_session = db.session
