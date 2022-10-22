from application.commons.commons import CommonModel
from application.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList


from application.utils.helper.string_processing_helper import clean_string

class LichSuDaoTao(CommonModel):

    __tablename__="lich_su_dao_tao"
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    nhan_vien_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"), nullable=True)
    ma_chuong_trinh =db.Column(db.String,nullable=True)
    ten_chuong_trinh =db.Column(db.String,nullable=True)
    tu_ngay = db.Column(db.BigInteger, nullable=True)
    den_ngay = db.Column(db.BigInteger, nullable=True)
    quy_doi_so_gio =db.Column(db.String,nullable=True)
    noi_dung_chuyen_mon =db.Column(db.String,nullable=True)
    chung_tu_dinh_kem = db.Column(MutableList.as_mutable(JSONB), default=[], nullable=True)
    trang_thai = db.Column(db.Boolean, default=True)
    thoi_gian_duyet = db.Column(db.BigInteger, nullable=True)
    ten_truong =db.Column(db.String,nullable=True)
    so_GCN_dao_tao =db.Column(db.String,nullable=True)
    ngay_cap_GCN = db.Column(db.BigInteger, nullable=True)
    so_tiet_hoc =db.Column(db.String,nullable=True)
    

    nguoi_duyet = db.relationship("User", backref="lich_su_dao_tao", lazy="joined")

    def __init__(self, nhan_vien_id=None,
                 ma_chuong_trinh=None, ten_chuong_trinh=None, tu_ngay=None, den_ngay=None,
                 quy_doi_so_gio=None, noi_dung_chuyen_mon=None, chung_tu_dinh_kem=[], 
                 trang_thai=None, thoi_gian_duyet=None,
                 ten_truong=None,so_GCN_dao_tao=None,ngay_cap_GCN=None,so_tiet_hoc=None):
        self.id = uuid.uuid4()
        self.nhan_vien_id = nhan_vien_id
        self.ma_chuong_trinh = ma_chuong_trinh
        self.quy_doi_so_gio = quy_doi_so_gio
        self.noi_dung_chuyen_mon = noi_dung_chuyen_mon  
        self.chung_tu_dinh_kem = chung_tu_dinh_kem   
        self.ten_chuong_trinh = ten_chuong_trinh
        self.tu_ngay = tu_ngay
        self.den_ngay = den_ngay
        self.trang_thai = trang_thai
        self.thoi_gian_duyet = thoi_gian_duyet
        self.ten_truong = ten_truong
        self.so_GCN_dao_tao = so_GCN_dao_tao
        self.ngay_cap_GCN = ngay_cap_GCN
        self.so_tiet_hoc = so_tiet_hoc
        