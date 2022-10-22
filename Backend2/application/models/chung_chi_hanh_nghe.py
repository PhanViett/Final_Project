from datetime import datetime
# from turtle import back
from itsdangerous import NoneAlgorithm
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from application.commons.commons import CommonModel
from application.extensions import db
from sqlalchemy import event
from sqlalchemy.orm import backref
from flask_jwt_extended import current_user
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from sqlalchemy.ext.mutable import MutableList

lk_pham_vi_chuyen_mon_cchn = db.Table(
"lk_pham_vi_chuyen_mon_cchn", db.Model.metadata,
db.Column("pham_vi_id", UUID(as_uuid=True),  db.ForeignKey('danhmuc_pham_vi_hoat_dong_chuyen_mon.id'), primary_key=True),
db.Column("cchn_id", UUID(as_uuid=True),  db.ForeignKey('chung_chi_hanh_nghe.id'), primary_key=True)
)

lk_vi_tri_hanh_nghe_cchn = db.Table(
"lk_vi_tri_hanh_nghe_cchn", db.Model.metadata,
db.Column("vi_tri_id", UUID(as_uuid=True),  db.ForeignKey('danhmuc_vi_tri_hanh_nghe.id'), primary_key=True),
db.Column("cchn_id", UUID(as_uuid=True),  db.ForeignKey('chung_chi_hanh_nghe.id'), primary_key=True)
)

class ChungChiHanhNghe(CommonModel):

    __tablename__ = "chung_chi_hanh_nghe"
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    nhan_vien_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"), nullable=True, unique=True)
    thoi_gian_yeu_cau_lien_ket = db.Column(db.BigInteger, nullable=True)
    thoi_gian_duyet_lien_ket = db.Column(db.BigInteger, nullable=True)
    thoi_gian_tu_choi_lien_ket = db.Column(db.BigInteger, nullable=True)
    ly_do_tu_choi = db.Column(db.TEXT, nullable=True)
    nguoi_duyet_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"), nullable=True)
    
    #* Văn bằng chuyên môn
    van_bang_chuyen_mon_id = db.Column(UUID(as_uuid=True), db.ForeignKey("danhmuc_van_bang_chuyen_mon.id"), nullable=True)

    #* Giấy phép
    so_giay_phep = db.Column(db.String, nullable=True)
    co_quan_cap = db.Column(db.String, nullable=True)
    ngay_hieu_luc = db.Column(db.BigInteger, nullable=True)
  
    phu_trach_chuyen_mon = db.Column(db.String, nullable=True)

    ngay_cap = db.Column(db.BigInteger, nullable=True)
    nam_cap = db.Column(db.String, nullable=True)
    noi_cap = db.Column(db.String, nullable=True)

    noi_cong_tac = db.Column(db.String, nullable=True)
    dia_chi_cong_tac = db.Column(db.String, nullable=True)
    
    loai_cap_chung_chi = db.Column(db.String, nullable=True)
    hinh_thuc_thi = db.Column(db.String, nullable=True)
    noi_dung_dieu_chinh =db.Column(db.TEXT, nullable=True)
    lan_cap_thu = db.Column(db.Integer, nullable=True)
    thay_the_chung_chi = db.Column(db.String, nullable=True)
    yeu_cau_phien_dich = db.Column(db.Boolean, default=False)
    so_quyet_dinh = db.Column(db.String, nullable=True)
    ngay_quyet_dinh = db.Column(db.BigInteger, nullable=True)

    #* Mục đính kèm
    dinh_kem_chung_chi = db.Column(MutableList.as_mutable(JSONB), nullable=True)
    dinh_kem_don_de_nghi = db.Column(MutableList.as_mutable(JSONB), nullable=True)
    dinh_kem_anh_chan_dung = db.Column(MutableList.as_mutable(JSONB), nullable=True)
    dinh_kem_van_bang_chuyen_mon = db.Column(MutableList.as_mutable(JSONB), nullable=True)
    dinh_kem_xac_nhan_suc_khoe = db.Column(MutableList.as_mutable(JSONB), nullable=True)
    dinh_kem_xac_nhan_thuc_hanh = db.Column(MutableList.as_mutable(JSONB), nullable=True)
    dinh_kem_xac_nhan_dao_tao= db.Column(MutableList.as_mutable(JSONB), nullable=True)
    dinh_kem_xac_nhan_cong_dan = db.Column(MutableList.as_mutable(JSONB), nullable=True)
    dinh_kem_xac_nhan_ly_lich = db.Column(MutableList.as_mutable(JSONB), nullable=True)
    dinh_kem_xac_nhan_cam_ket = db.Column(MutableList.as_mutable(JSONB), nullable=True)
    dinh_kem_xac_nhan_le_phi = db.Column(MutableList.as_mutable(JSONB), nullable=True)
    dinh_kem_xac_nhan_thay_doi = db.Column(MutableList.as_mutable(JSONB), nullable=True)
    dinh_kem_xac_nhan_khac = db.Column(MutableList.as_mutable(JSONB), nullable=True)
    
    ghi_chu = db.Column(db.String, nullable=True)
    ghi_chu_pham_vi_hanh_nghe = db.Column(db.String, nullable=True)
    ghi_chu_vi_tri_hanh_nghe = db.Column(db.String, nullable=True)

    #* Trạng thái
    trang_thai_ho_so = db.Column(db.String, nullable=True)
    
    nhan_vien = db.relationship("User", foreign_keys=[nhan_vien_id], back_populates="chung_chi_hanh_nghe", lazy="joined", uselist=False)
    
    pham_vi_chuyen_mon = db.relationship("PhamViHoatDongChuyenMon", secondary="lk_pham_vi_chuyen_mon_cchn",
                                 cascade="delete",  lazy="subquery", backref=db.backref("chung_chi_hanh_nghe", lazy=True))
    vi_tri_hanh_nghe = db.relationship("ViTriHanhNghe", secondary="lk_vi_tri_hanh_nghe_cchn",
                                 cascade="delete",  lazy="subquery", backref=db.backref("chung_chi_hanh_nghe", lazy=True))
    van_bang_chuyen_mon = db.relationship("VanBangChuyenMon", foreign_keys=[van_bang_chuyen_mon_id],back_populates="chung_chi_hanh_nghe", lazy="joined")


    def __init__(
        self,
        nhan_vien_id = None,
        van_bang_chuyen_mon_id=None,
        thoi_gian_yeu_cau_lien_ket = None,
        thoi_gian_duyet_lien_ket = None,
        thoi_gian_tu_choi_lien_ket = None,
        ly_do_tu_choi = None,
        nguoi_duyet_id = None,
        so_giay_phep = None,
        co_quan_cap = None,
        ngay_hieu_luc = None,
        ngay_cap =None,
        noi_cap = None,
        nam_cap = None,
        noi_cong_tac = None,
        dia_chi_cong_tac = None,
        loai_cap_chung_chi = None,
        hinh_thuc_thi = None,
        noi_dung_dieu_chinh = None,
        lan_cap_thu = None,
        thay_the_chung_chi = None,
        yeu_cau_phien_dich = None,
        so_quyet_dinh = None,
        ngay_quyet_dinh = None,
        dinh_kem_chung_chi=None,
        dinh_kem_don_de_nghi=None,
        dinh_kem_anh_chan_dung=None,
        dinh_kem_van_bang_chuyen_mon=None,
        dinh_kem_xac_nhan_suc_khoe=None,
        dinh_kem_xac_nhan_thuc_hanh=None,
        dinh_kem_xac_nhan_dao_tao=None,
        dinh_kem_xac_nhan_cong_dan=None,
        dinh_kem_xac_nhan_ly_lich=None,
        dinh_kem_xac_nhan_cam_ket=None,
        dinh_kem_xac_nhan_le_phi=None,
        dinh_kem_xac_nhan_thay_doi=None,
        dinh_kem_xac_nhan_khac=None,
        trang_thai_ho_so='0',
        ghi_chu=None,
        ghi_chu_pham_vi_hanh_nghe=None,
        ghi_chu_vi_tri_hanh_nghe=None,
        phu_trach_chuyen_mon=None
    ) :
        self.nhan_vien_id = nhan_vien_id
        self.thoi_gian_yeu_cau_lien_ket = thoi_gian_yeu_cau_lien_ket
        self.thoi_gian_duyet_lien_ket = thoi_gian_duyet_lien_ket
        self.thoi_gian_tu_choi_lien_ket = thoi_gian_tu_choi_lien_ket
        self.ly_do_tu_choi = ly_do_tu_choi
        self.nguoi_duyet_id = nguoi_duyet_id
        self.hinh_thuc_thi = hinh_thuc_thi
        self.so_giay_phep = so_giay_phep
        self.co_quan_cap = co_quan_cap
        self.ngay_hieu_luc = ngay_hieu_luc
        self.ngay_cap = ngay_cap
        self.noi_cap = noi_cap

        self.nam_cap = nam_cap
        self.noi_cong_tac = noi_cong_tac
        self.dia_chi_cong_tac = dia_chi_cong_tac
        self.loai_cap_chung_chi = loai_cap_chung_chi
        self.noi_dung_dieu_chinh = noi_dung_dieu_chinh
        self.lan_cap_thu = lan_cap_thu
        self.thay_the_chung_chi = thay_the_chung_chi
        self.yeu_cau_phien_dich = yeu_cau_phien_dich
        self.so_quyet_dinh = so_quyet_dinh
        self.ngay_quyet_dinh = ngay_quyet_dinh
        self.dinh_kem_chung_chi = dinh_kem_chung_chi
        self.dinh_kem_don_de_nghi = dinh_kem_don_de_nghi
        self.dinh_kem_anh_chan_dung = dinh_kem_anh_chan_dung
        self.dinh_kem_van_bang_chuyen_mon = dinh_kem_van_bang_chuyen_mon
        self.dinh_kem_xac_nhan_suc_khoe = dinh_kem_xac_nhan_suc_khoe
        self.dinh_kem_xac_nhan_thuc_hanh = dinh_kem_xac_nhan_thuc_hanh
        self.dinh_kem_xac_nhan_dao_tao = dinh_kem_xac_nhan_dao_tao
        self.dinh_kem_xac_nhan_cong_dan = dinh_kem_xac_nhan_cong_dan
        self.dinh_kem_xac_nhan_ly_lich = dinh_kem_xac_nhan_ly_lich
        self.dinh_kem_xac_nhan_cam_ket = dinh_kem_xac_nhan_cam_ket
        self.dinh_kem_xac_nhan_le_phi = dinh_kem_xac_nhan_le_phi
        self.dinh_kem_xac_nhan_thay_doi = dinh_kem_xac_nhan_thay_doi
        self.dinh_kem_xac_nhan_khac = dinh_kem_xac_nhan_khac
        self.trang_thai_ho_so = trang_thai_ho_so
        self.van_bang_chuyen_mon_id = van_bang_chuyen_mon_id
        self.ghi_chu =ghi_chu
        self.ghi_chu_pham_vi_hanh_nghe = ghi_chu_pham_vi_hanh_nghe
        self.ghi_chu_vi_tri_hanh_nghe =ghi_chu_vi_tri_hanh_nghe
        self.phu_trach_chuyen_mon = phu_trach_chuyen_mon

@event.listens_for(ChungChiHanhNghe, "before_insert")
def on_insert_trigger(mapper, connection, target):
    verify_jwt_in_request()
    target.created_at = datetime.now()
    target.created_by = current_user.id


@event.listens_for(ChungChiHanhNghe, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.now()