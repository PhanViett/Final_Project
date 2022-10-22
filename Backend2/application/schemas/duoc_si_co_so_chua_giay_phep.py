from application.extensions import ma, db
from application.models.duoc_si_co_so import DuocSiCoSo
from marshmallow import fields

from application.models.duoc_si_co_so_chua_giay_phep import DuocSiCoSoChuaGiayPhep


class DuocSiCoSoChuaGiayPhepSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)

    class Meta:
        model = DuocSiCoSoChuaGiayPhep
        include_fk = True
        # include_relationship = True
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at", "deleted", "created_by", "updated_by")
