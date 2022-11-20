
from sqlalchemy.dialects.postgresql import UUID, SMALLINT
import uuid
from application.extensions import db
from sqlalchemy import event, func, Index
from flask_jwt_extended import current_user
from application.utils.helper.convert_timestamp_helper import get_current_time


class TinTuc(db.Model):

    __tablename__ = "tin_tuc"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=True)

    ref_name = db.Column(db.String, nullable=True)
    ref_logo = db.Column(db.String, nullable=True)
    ref_link = db.Column(db.String, nullable=True)

    created_at = db.Column(db.String, nullable=True)
    created_by = db.Column(db.String, nullable=True)
    updated_at = db.Column(db.String, nullable=True)
    updated_by = db.Column(db.String, nullable=True)
    accepted_by = db.Column(db.String, nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String, nullable=True)
    deleted_at = db.Column(db.String, nullable=True)


@ event.listens_for(TinTuc, "before_insert")
def on_update_trigger(mapper, connection, target: TinTuc):
    target.created_at = get_current_time("int")
    target.updated_at = get_current_time("int")
    target.created_by = current_user.id if current_user else None
    target.updated_at = current_user.id if current_user else None

@event.listens_for(TinTuc, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = get_current_time("int")
    target.updated_at = current_user.id if current_user else None
