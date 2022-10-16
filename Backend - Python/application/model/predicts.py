import uuid
from datetime import datetime
from application.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from application.utils.helper.string_processing_helper import clean_string


class Predicts(db.Model):
    created_at = db.Column(db.BigInteger, default=int(datetime.utcnow().timestamp()), nullable=True)
    updated_at = db.Column(db.BigInteger, default=int(datetime.utcnow().timestamp()), nullable=True)

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=True)
    result = db.Column(db.Boolean, nullable=True)

    def __init__(self, user_id=None, result=None):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.result = result