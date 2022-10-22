from application.extensions import ma, db
from application.models.chung_chi_hanh_nghe import ChungChiHanhNghe
from application.models.chung_nhan_thuc_hanh_co_so import ChungNhanCoSo
from application.models.co_so_kinh_doanh import CoSoKinhDoanh
from application.schemas.danhmuc_loai_hình_kinh_doanh import LoaiHinhKinhDoanhSchema
from application.schemas.danhmuc_pham_vi_hoat_dong_kinh_doanh import PhamVihoatDongKinhDoanhSchema
from marshmallow import fields

class ChungNhanCoSoSchema(ma.SQLAlchemyAutoSchema):
     id = ma.auto_field(dump_only=True)
     # coso_kinhdoanh_id = ma.auto_field()
     # quan_huyen_id = ma.auto_field()
     # tinh_thanh_id = ma.auto_field()
     # xa_phuong_id = ma.auto_field()
     # coso_kinhdoanh_id = ma.auto_field()




     class Meta:
            model = ChungNhanCoSo
            include_fk = True
            # include_relationship = True
            sqla_session = db.session
            load_instance = True
            exclude = ("created_at", "updated_at", "deleted_at", "deleted","created_by","updated_by")