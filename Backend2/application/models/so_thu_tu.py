from application.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from application.commons.commons import CommonModel



class SoThuTu(CommonModel):
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    loai = db.Column(db.String, nullable=True)
    so_thu_tu = db.Column(db.Integer, nullable=True)


    def __init__(self, loai=None, so_thu_tu=None):
        self.id = uuid.uuid4()
        self.loai = loai
        self.so_thu_tu = so_thu_tu