import uuid
from datetime import datetime
from application.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from application.utils.helper.string_processing_helper import clean_string

class News(db.Model):
    __tablename__ = 'news'
    created_at = db.Column(db.BigInteger, default=int(datetime.utcnow().timestamp()), nullable=True)
    updated_at = db.Column(db.BigInteger, default=int(datetime.utcnow().timestamp()), nullable=True)
    created_by = db.Column(db.String, nullable=True)
    updated_by = db.Column(db.String, nullable=True)
    accepted_by = db.Column(db.String, nullable=True)

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    tags = db.Column(db.String, nullable=True)

def __init__(self, created_by = None, updated_by = None, accepted_by = None, 
                title = None, description = None, tags = None):
    self.id = uuid.uuid4()
    self.created_by = created_by
    self.updated_by = updated_by
    self.accepted_by = accepted_by
    self.title = title
    self.description = description
    self.tags = tags
