import uuid
from sqlalchemy import event
from application.extensions import db
from sqlalchemy.dialects.postgresql.base import UUID
from application.utils.helper.convert_timestamp_helper import get_current_time
from application.commons.commons import CommonModel


class Records(CommonModel):
    __tablename__ = "records"

    # created_at = db.Column(db.BigInteger, nullable=True)
    # updated_at = db.Column(db.BigInteger, nullable=True)

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=True)
    tuoi = db.Column(db.BigInteger, nullable=True)
    gioi_tinh = db.Column(db.BigInteger, nullable=True)
    height = db.Column(db.BigInteger, nullable=True)
    weight = db.Column(db.BigInteger, nullable=True)
    ap_hi = db.Column(db.BigInteger, nullable=True)
    ap_lo = db.Column(db.BigInteger, nullable=True)
    chol = db.Column(db.BigInteger, nullable=True)
    gluc = db.Column(db.BigInteger, nullable=True)
    smoke = db.Column(db.BigInteger, nullable=True)
    alco = db.Column(db.BigInteger, nullable=True)
    active = db.Column(db.BigInteger, nullable=True)
    result = db.Column(db.BigInteger, nullable=True)

    users = db.relationship("Users", foreign_keys=[user_id], back_populates="records", lazy="joined", uselist=False)


    def __init__(self, user_id=None, tuoi=None, gioi_tinh=None, height=None,
                 weight=None, ap_hi=None, ap_lo=None, chol=None, gluc=None, smoke=None,
                 alco=None, active=None, result=None):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.tuoi = tuoi
        self.gioi_tinh = gioi_tinh
        self.height = height
        self.weight = weight
        self.ap_hi = ap_hi
        self.ap_lo = ap_lo
        self.chol = chol
        self.gluc = gluc
        self.smoke = smoke        
        self.alco = alco
        self.active = active
        self.result = result

@ event.listens_for(Records, "before_insert")
def on_update_trigger(mapper, connection, target: Records):
    target.created_at = get_current_time("int")
    target.updated_at = get_current_time("int")


@event.listens_for(Records, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = get_current_time("int")
