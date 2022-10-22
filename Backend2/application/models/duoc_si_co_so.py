
from application.commons.commons import CommonModel
from application.extensions import db
import uuid
import datetime
from sqlalchemy import event
from sqlalchemy.dialects.postgresql import UUID


class DuocSiCoSo(CommonModel):
    __tablename__ = "duoc_si_co_so"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    duoc_si_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"),  unique=True, nullable=True)
    co_so_kinh_doanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("co_so_kinh_doanh.id"), nullable=True)
    vai_tro = db.Column(db.SmallInteger, nullable=True)

    co_so_kinh_doanh = db.relationship("CoSoKinhDoanh", foreign_keys=[co_so_kinh_doanh_id], uselist=False)
    duoc_si = db.relationship("User", foreign_keys=[duoc_si_id], uselist=False, back_populates="duoc_si_co_so")

    def __init__(
        self,
        duoc_si_id=None,
        co_so_kinh_doanh_id=None,
        vai_tro=None
    ):
        self.id = uuid.uuid4()
        self.duoc_si_id = duoc_si_id
        self.co_so_kinh_doanh_id = co_so_kinh_doanh_id
        self.vai_tro = vai_tro


@event.listens_for(DuocSiCoSo, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(DuocSiCoSo, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()
