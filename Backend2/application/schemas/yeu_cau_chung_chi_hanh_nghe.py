import io
import json
from application.extensions import ma, db
from marshmallow import fields
from application.models.yeu_cau_chung_chi_hanh_nghe import YeuCauChungChiHanhNghe


class YeuCauChungChiHanhNgheSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    thu_tuc_id = ma.auto_field()
    loai_ma_cchnd = ma.auto_field()
    hoi_dong_id = ma.auto_field()
    updated_at = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    # trang_thai_ho_so = fields.Method("check_trang_thai_value")
    # nhan_vien_id = ma.auto_field() Ch

    class Meta:
        model = YeuCauChungChiHanhNghe
        sqla_session = db.session
        load_instance = True
        exclude = ("deleted_at", "deleted", "created_by", "updated_by", "trang_thai_het_han")

    def check_trang_thai_value(self, object):
        f = open('application/jsonFile/trang_thai_ho_so.json', encoding='utf-8')
        trang_thai_jsonLoad = json.load(f)
        if object.trang_thai_ho_so in trang_thai_jsonLoad:
            return trang_thai_jsonLoad[object.trang_thai_ho_so]


class YeuCauChungChiHanhNgheGetListPaginateSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    thu_tuc_id = ma.auto_field()
    # trang_thai_ho_so = fields.Method("check_trang_thai_value")
    ten_thu_tuc = fields.String(attribute="thu_tuc.ten")
    ten_nguoi_yeu_cau = fields.String(attribute="duoc_si.ten")

    # nhan_vien_id = ma.auto_field()

    class Meta:
        model = YeuCauChungChiHanhNghe
        sqla_session = db.session
        load_instance = True
        exclude = ("updated_at", "deleted_at", "deleted", "created_by", "updated_by", "trang_thai_het_han")

    def check_trang_thai_value(self, object):
        f = open('application/jsonFile/trang_thai_ho_so.json', encoding='utf-8')
        trang_thai_jsonLoad = json.load(f)
        if object.trang_thai_ho_so in trang_thai_jsonLoad:
            return trang_thai_jsonLoad[object.trang_thai_ho_so]
