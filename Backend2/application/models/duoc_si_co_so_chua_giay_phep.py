
from application.commons.commons import CommonModel
from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.mutable import MutableList
from application.utils.helper.string_processing_helper import clean_string


class DuocSiCoSoChuaGiayPhep(CommonModel):
    __tablename__ = "duoc_si_co_so_chua_giay_phep"

    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    ho_ten = db.Column(db.String,nullable=True)
    ngay_sinh = db.Column(db.BigInteger, nullable=True)
    gioi_tinh = db.Column(db.SmallInteger,nullable=True)
    so_dien_thoai = db.Column(db.String,nullable=True)
    cmnd_cccd = db.Column(db.String,nullable=True)
    bang_cap = db.Column(db.String,nullable=True)
    vi_tri_lam_viec = db.Column(MutableList.as_mutable(JSONB),nullable=True)
    dia_chi = db.Column(db.String,nullable=True)
    co_so_kinh_doanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("co_so_kinh_doanh.id"), nullable=True)
    quan_huyen_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quan_huyen.id"), nullable=True)
    tinh_thanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tinh_thanh.id"), nullable=True)
    xa_phuong_id = db.Column(UUID(as_uuid=True), db.ForeignKey("xa_phuong.id"), nullable=True)
    
    co_so_kinh_doanh = db.relationship("CoSoKinhDoanh", foreign_keys=[co_so_kinh_doanh_id], back_populates="duoc_si_co_so_chua_giay_phep")
    
    def __init__(
        self,
        ho_ten = None,
        ngay_sinh= None,  
        gioi_tinh =None,
        dia_chi =None,
        so_dien_thoai =None,
        cmnd_cccd =None,
        bang_cap =None,
        vi_tri_lam_viec =None,
        co_so_kinh_doanh_id =None,
        quan_huyen_id =None,
        tinh_thanh_id =None,
        xa_phuong_id =None
    ):
        self.ho_ten = ho_ten
        self.ngay_sinh = ngay_sinh
        self.gioi_tinh = gioi_tinh
        self.so_dien_thoai = so_dien_thoai
        self.dia_chi = dia_chi
        self.cmnd_cccd = cmnd_cccd
        self.bang_cap = bang_cap
        self.vi_tri_lam_viec = vi_tri_lam_viec
        self.co_so_kinh_doanh_id = co_so_kinh_doanh_id
        self.quan_huyen_id = quan_huyen_id
        self.tinh_thanh_id =tinh_thanh_id
        self.xa_phuong_id = xa_phuong_id
        
        
        
        
       
        
        
        
        
        
        
       
      
       


