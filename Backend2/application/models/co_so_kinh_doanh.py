
from application.commons.commons import CommonModel
from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from application.models.duoc_si_co_so import DuocSiCoSo
from sqlalchemy import and_
from application.utils.helper.string_processing_helper import clean_string


class CoSoKinhDoanh(CommonModel):
    __tablename__ = "co_so_kinh_doanh"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_mapping = db.Column(db.String)
    taikhoan_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tai_khoan.id"), nullable=True)

    tinh_thanh_coso_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tinh_thanh.id"), nullable=True)
    quan_huyen_coso_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quan_huyen.id"), nullable=True)
    xa_phuong_coso_id = db.Column(UUID(as_uuid=True), db.ForeignKey("xa_phuong.id"), nullable=True)

    tinh_thanh_tructhuoc_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tinh_thanh.id"), nullable=True)
    quan_huyen_tructhuoc_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quan_huyen.id"), nullable=True)
    xa_phuong_tructhuoc_id = db.Column(UUID(as_uuid=True), db.ForeignKey("xa_phuong.id"), nullable=True)

    ma_coso = db.Column(db.String, nullable=True)
    ten_coso = db.Column(db.String, nullable=True)
    ten_coso_khongdau = db.Column(db.String, nullable=True)
    email_coso = db.Column(db.String, nullable=True)
    dienthoai_coso = db.Column(db.String, nullable=True)
    avatar_url = db.Column(db.String, nullable=True)
    trang_thai = db.Column(db.String, default="0")
    diachi_coso = db.Column(db.String, nullable=True)
    fax_coso = db.Column(db.String, nullable=True)
    ten_kinhdoanh = db.Column(db.String, nullable=True)
    ten_kinhdoanh_khongdau = db.Column(db.String, nullable=True)
    so_nha_kinh_doanh = db.Column(db.String)
    diachi_kinh_doanh = db.Column(db.String, nullable=True)
    ten_nguoi_lien_he = db.Column(db.String, nullable=True)
    chuc_danh_nguoi_lienhe = db.Column(db.String, nullable=True)
    email_nguoi_lienhe = db.Column(db.String, nullable=True)
    dien_thoai_nguoi_lienhe = db.Column(db.String, nullable=True)
    fax_nguoi_lienhe = db.Column(db.String, nullable=True)
    dia_chi_nguoi_lien_he = db.Column(db.String, nullable=True)
    chung_minh_nguoi_lien_he = db.Column(db.String, nullable=True)

    truc_thuoc = db.Column(db.String, nullable=True)
    ten_truc_thuoc = db.Column(db.String, nullable=True)
    ten_truc_thuoc_khong_dau = db.Column(db.String, nullable=True)
    diachi_tructhuoc = db.Column(db.String, nullable=True)
    website_co_so = db.Column(db.String, nullable=True)
    ma_tructhuoc = db.Column(db.String, nullable=True)
    maso_doanh_nghiep_kinh_doanh = db.Column(db.String, nullable=True)
    ma_so_doanh_nghiep_chi_nhanh = db.Column(db.String, nullable=True)

    da_cap_giay_phep = db.Column(db.Boolean, default=False)

    so_gcn = db.Column(db.Integer, nullable=True)
    loai_gcn = db.Column(db.String, nullable=True)
    ngay_cap_gcn = db.Column(db.BigInteger, nullable=True)
    ngay_het_han_gcn = db.Column(db.BigInteger, nullable=True)
    ngay_nop_gcn = db.Column(db.BigInteger, nullable=True)
    so_ptn_gcn = db.Column(db.Integer, nullable=True)
    chuyen_vien_xu_ly_gcn = db.Column(db.String, nullable=True)

    tinh_thanh = db.relationship("TinhThanh", foreign_keys=[tinh_thanh_coso_id], uselist=False)
    quan_huyen = db.relationship("QuanHuyen", foreign_keys=[quan_huyen_coso_id], uselist=False)
    xa_phuong = db.relationship("XaPhuong", foreign_keys=[xa_phuong_coso_id], uselist=False)
    giay_phep_kinh_doanh = db.relationship(
        "GiayPhepKinhDoanh", foreign_keys="GiayPhepKinhDoanh.co_so_kinh_doanh_id", back_populates="co_so_kinh_doanh", uselist=False)
    duoc_si_co_so_chua_giay_phep = db.relationship(
        "DuocSiCoSoChuaGiayPhep", uselist=True, back_populates="co_so_kinh_doanh")

    duoc_si_ctncm = db.relationship("DuocSiCoSo", uselist=False,
                                    primaryjoin=and_(id == DuocSiCoSo.co_so_kinh_doanh_id, DuocSiCoSo.vai_tro == 0),
                                    foreign_keys=[DuocSiCoSo.co_so_kinh_doanh_id], viewonly=True)

    duoc_si_ctncl = db.relationship("DuocSiCoSo", uselist=True,
                                    primaryjoin=and_(id == DuocSiCoSo.co_so_kinh_doanh_id, DuocSiCoSo.vai_tro == 1),
                                    foreign_keys=[DuocSiCoSo.co_so_kinh_doanh_id], viewonly=True)
    tai_khoan = db.relationship("TaiKhoan", foreign_keys=[taikhoan_id], backref="co_so_kinh_doanh_id")

    def __init__(
        self,
        taikhoan_id=None,
        ma_coso=None,
        ten_coso=None,
        email_coso=None,
        dienthoai_coso=None,
        avatar_url=None,
        fax_coso=None,
        dinhkem_chungchi=None,
        dinhkem_anh_chandung=None,
        dinhkem_vanbang_chuyenmon=None,
        dinhkem_xacnhan_congdan=None,
        dinhkem_files_khac=None,
        trang_thai=None,
        diachi_coso=None,
        ten_kinhdoanh=None,
        ten_nguoi_lien_he=None,
        chuc_danh_nguoi_lienhe=None,
        email_nguoi_lienhe=None,
        dien_thoai_nguoi_lienhe=None,
        fax_nguoi_lienhe=None,
        truc_thuoc=None,
        ten_truc_thuoc=None,
        diachi_tructhuoc=None,
        website_co_so=None,
        chung_minh_nguoi_lien_he=None,
        ma_tructhuoc=None,
        maso_doanh_nghiep_kinh_doanh=None,
        ma_so_doanh_nghiep_chi_nhanh=None,
        dia_chi_nguoi_lien_he=None,
        tinh_thanh_coso_id=None,
        quan_huyen_coso_id=None,
        xa_phuong_coso_id=None,
        tinh_thanh_tructhuoc_id=None,
        quan_huyen_tructhuoc_id=None,
        xa_phuong_tructhuoc_id=None,
        id_mapping=None,
        so_nha_kinh_doanh=None

    ):
        self.id = uuid.uuid4()
        self.taikhoan_id = taikhoan_id
        self.ma_coso = ma_coso
        self.ten_coso = ten_coso
        self.ten_coso_khongdau = clean_string(ten_coso)
        self.email_coso = email_coso
        self.dienthoai_coso = dienthoai_coso
        self.avatar_url = avatar_url
        self.dinhkem_chungchi = dinhkem_chungchi
        self.dinhkem_anh_chandung = dinhkem_anh_chandung
        self.dinhkem_vanbang_chuyenmon = dinhkem_vanbang_chuyenmon
        self.dinhkem_xacnhan_congdan = dinhkem_xacnhan_congdan
        self.dinhkem_files_khac = dinhkem_files_khac
        self.trang_thai = trang_thai
        self.diachi_coso = diachi_coso
        self.ten_kinhdoanh = ten_kinhdoanh
        self.ten_kinhdoanh_khongdau = clean_string(ten_kinhdoanh) if ten_kinhdoanh else None
        self.ten_nguoi_lien_he = ten_nguoi_lien_he
        self.chuc_danh_nguoi_lienhe = chuc_danh_nguoi_lienhe
        self.email_nguoi_lienhe = email_nguoi_lienhe
        self.dien_thoai_nguoi_lienhe = dien_thoai_nguoi_lienhe
        self.fax_nguoi_lienhe = fax_nguoi_lienhe
        self.truc_thuoc = truc_thuoc
        self.ten_truc_thuoc = ten_truc_thuoc
        self.ten_truc_thuoc_khong_dau = clean_string(ten_truc_thuoc) if ten_truc_thuoc else None
        self.diachi_tructhuoc = diachi_tructhuoc
        self.website_co_so = website_co_so
        self.chung_minh_nguoi_lien_he = chung_minh_nguoi_lien_he
        self.ma_tructhuoc = ma_tructhuoc
        self.maso_doanh_nghiep_kinh_doanh = maso_doanh_nghiep_kinh_doanh
        self.ma_so_doanh_nghiep_chi_nhanh = ma_so_doanh_nghiep_chi_nhanh
        self.dia_chi_nguoi_lien_he = dia_chi_nguoi_lien_he
        self.tinh_thanh_coso_id = tinh_thanh_coso_id
        self.quan_huyen_coso_id = quan_huyen_coso_id
        self.xa_phuong_coso_id = xa_phuong_coso_id
        self.tinh_thanh_tructhuoc_id = tinh_thanh_tructhuoc_id
        self.quan_huyen_tructhuoc_id = quan_huyen_tructhuoc_id
        self.xa_phuong_tructhuoc_id = xa_phuong_tructhuoc_id
        self.id_mapping = id_mapping
        self.fax_coso = fax_coso
        self.so_nha_kinh_doanh = so_nha_kinh_doanh

        # self.is_super_admin = is_super_admin
