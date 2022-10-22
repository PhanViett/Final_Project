
from application.commons.commons import CommonModel
from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID



class LichSuChungChi(CommonModel):
    __tablename__ = "lich_su_chung_chi"

    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"), nullable=True)
    loai_thay_doi = db.Column(db.String,nullable=True)
    noi_dung_thay_doi = db.Column(db.String,nullable=True)
    ngay_thay_doi = db.Column(db.BigInteger,nullable=True)
    so_quyet_dinh = db.Column(db.String,nullable=True)
    chung_tu_dinh_kem = db.Column(db.String,nullable=True)
    chung_chi_cu = db.Column(db.String,nullable=True)
    chung_chi_moi = db.Column(db.String,nullable=True)
    chuyen_vien_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"), nullable=True)
    lanh_dao_id = db.Column(UUID(as_uuid=True), db.ForeignKey("nhan_vien.id"), nullable=True)
    trang_thai = db.Column(db.Boolean,nullable=True,default =True)
    
    def __init__(
        self,
        user_id = None,
        loai_thay_doi= None,  
        noi_dung_thay_doi =None,
        ngay_thay_doi =None,
        so_quyet_dinh =None,
        chung_tu_dinh_kem =None,
        chung_chi_cu =None,
        chung_chi_moi =None,
        chuyen_vien_id =None,
        lanh_dao_id =None,
        trang_thai =None,     
    ):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.loai_thay_doi = loai_thay_doi
        self.noi_dung_thay_doi = noi_dung_thay_doi
        self.ngay_thay_doi = ngay_thay_doi
        self.so_quyet_dinh = so_quyet_dinh
        self.chung_tu_dinh_kem = chung_tu_dinh_kem
        self.chung_chi_cu = chung_chi_cu
        self.chung_chi_moi = chung_chi_moi
        self.chuyen_vien_id = chuyen_vien_id
        self.lanh_dao_id = lanh_dao_id   
        self.trang_thai = trang_thai
       
        
        
        
        
       
        
        
        
        
        
        
       
      
       


