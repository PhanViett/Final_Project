
from marshmallow import fields
from yaml import dump
from application.extensions import ma, db
from application.models.bang_cap import BangCap
from marshmallow import post_dump

from application.models.danhmuc_noi_tot_nghiep import NoiTotNghiep
from application.models.danhmuc_van_bang_chuyen_mon import VanBangChuyenMon
from sqlalchemy import cast, String


class BangCapSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    noi_tot_nghiep = fields.Str(attribute="noi_tot_nghiep.ten", allow_none=True, dump_default=None)
    van_bang_chuyen_mon = fields.Str(attribute="van_bang_chuyen_mon.ten", allow_none=True, dump_default=None)
    noi_tot_nghiep_id = ma.auto_field()
    van_bang_chuyen_mon_id = ma.auto_field()

    class Meta:
        model = BangCap
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at", "deleted", "created_by", "updated_by", "deleted_by")


class BangCapDuocSiSchema(ma.SQLAlchemySchema):
    id = ma.auto_field(dump_only=True)
    so_hieu = ma.auto_field(dump_only=True)
    chung_tu_dinh_kem = ma.auto_field(dump_only=True)
    van_bang_chuyen_mon_id = ma.auto_field(dump_only=True)
    noi_tot_nghiep_id = ma.auto_field(dump_only=True)
    ngay_cap = ma.auto_field(dump_only=True)
    xep_hang = ma.auto_field(dump_only=True)
    hinh_thuc_dao_tao = ma.auto_field(dunp_only=True)

    class Meta:
        model = BangCap
        sqla_session = db.session
        load_instance = True

    @post_dump(pass_many=True)
    def after_dumping(self, data, **kwargs):

        noi_tot_nghiep_map = {x.id: x.ten for x in db.session.query(
            cast(NoiTotNghiep.id, String).label("id"), NoiTotNghiep.ten.label("ten")).all()}
        van_bang_map = {x.id: x.ten for x in db.session.query(
            cast(VanBangChuyenMon.id, String).label("id"), VanBangChuyenMon.ten.label("ten")).all()}
        for item in data:
            item["van_bang_chuyen_mon"] = van_bang_map.get(
                item["van_bang_chuyen_mon_id"]) if item.get("van_bang_chuyen_mon_id") else None
            item["noi_tot_nghiep"] = noi_tot_nghiep_map.get(
                item["noi_tot_nghiep_id"]) if item.get("noi_tot_nghiep_id") else None
        db.session.commit()
        return data


class BangCapNguoiHanhNgheSchema(ma.SQLAlchemySchema):
    noi_tot_nghiep = fields.Str(attribute="noi_tot_nghiep.ten", allow_none=True, dump_default=None)
    van_bang_chuyen_mon = fields.Str(attribute="van_bang_chuyen_mon.ten", allow_none=True, dump_default=None)
    nam_tot_nghiep = fields.String(attribute="nam_cap", allow_none=True, dump_default=None, dump_only=True)

    class Meta:
        model = BangCap
        sqla_session = db.session
        load_instance = True
