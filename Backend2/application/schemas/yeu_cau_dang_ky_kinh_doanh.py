import json
from application.extensions import ma, db
from marshmallow import fields
from application.models.yeu_cau_dang_ky_kinh_doanh import YeuCauDangKyKinhDoanh


class YeuCauDangKyKinhDoanhSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    thu_tuc_id = ma.auto_field()
    trang_thai_ho_so = fields.Method("check_trang_thai_value")

    class Meta:
        model = YeuCauDangKyKinhDoanh
        sqla_session = db.session
        load_instance = True
        exclude = ("created_at", "updated_at", "deleted_at", "deleted", "created_by", "updated_by")

    def check_trang_thai_value(self, object):
        f = open('trang_thai_ho_so.json', encoding='utf-8')
        trang_thai_jsonLoad = json.load(f)
        if object.trang_thai_ho_so in trang_thai_jsonLoad:
            return trang_thai_jsonLoad[object.trang_thai_ho_so]
