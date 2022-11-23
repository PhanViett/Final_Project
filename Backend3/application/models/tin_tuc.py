
from sqlalchemy.dialects.postgresql import UUID, SMALLINT
import uuid
from application.extensions import db
from sqlalchemy import event, func, Index
from flask_jwt_extended import current_user
from application.utils.helper.convert_timestamp_helper import get_current_time


class TinTuc(db.Model):

    __tablename__ = "tin_tuc"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=True)
    
    title = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=True)
    status = db.Column(db.Integer, nullable=True)
    views =  db.Column(db.BigInteger, nullable=True)
    thumbnail = db.Column(db.String, nullable=True)

    ref_name = db.Column(db.String, nullable=True)
    ref_logo = db.Column(db.String, nullable=True)
    ref_link = db.Column(db.String, nullable=True)

    created_at = db.Column(db.String, nullable=True)
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=True)
    updated_at = db.Column(db.String, nullable=True)
    updated_by = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=True)
    accepted_by = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String, nullable=True)
    deleted_at = db.Column(db.String, nullable=True)

    users = db.relationship("Users", foreign_keys=[user_id], back_populates="tintuc", lazy="joined", uselist=False)


def __init__(self, user_id=None, title=None, content=None, status=None, views=None):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.title = title
        self.content = content
        self.status = status
        self.views = 0


@ event.listens_for(TinTuc, "before_insert")
def on_update_trigger(mapper, connection, target: TinTuc):
    target.created_at = get_current_time("int")
    target.updated_at = get_current_time("int")
    target.created_by = current_user.id if current_user else None
    target.updated_by = current_user.id if current_user else None
    target.views = 0

@event.listens_for(TinTuc, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = get_current_time("int")
    target.updated_at = current_user.id if current_user else None
