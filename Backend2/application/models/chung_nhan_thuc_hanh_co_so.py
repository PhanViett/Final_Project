
import datetime
from sqlalchemy import true
from application.commons.commons import CommonModel
from application.extensions import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import event
from application.utils.helper.string_processing_helper import clean_string


class ChungNhanCoSo(CommonModel):
    __tablename__ = "chung_nhan_thuc_hanh_co_so"

    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    so_giaychungnhan = db.Column(db.String,nullable=True)
    ngay_kiemtra = db.Column(db.BigInteger, nullable= True)
    ngay_cap = db.Column(db.BigInteger, nullable= True)
    ngay_hieu_luc = db.Column(db.BigInteger, nullable= True)
    ngay_het_han = db.Column(db.BigInteger, nullable= True)
    diachi = db.Column(db.String,nullable=True)
    quan_huyen_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quan_huyen.id"), nullable=True)
    tinh_thanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tinh_thanh.id"), nullable=True)
    xa_phuong_id = db.Column(UUID(as_uuid=True), db.ForeignKey("xa_phuong.id"), nullable=True)
    dinhkem_giaychungnhan = db.Column(db.String,nullable=True)
    coso_kinhdoanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("co_so_kinh_doanh.id"), nullable=True)
    trang_thai = db.Column(db.Boolean,nullable=True,default = True)
    
    
    def __init__(
        self,
        so_giaychungnhan = None,
        ngay_kiemtra= None,  
        ngay_cap =None,
        ngay_hieu_luc=None,
        ngay_het_han =None,
        diachi =None,
        dinhkem_giaychungnhan =None,
        coso_kinhdoanh_id =None,
        trang_thai =None,
        quan_huyen_id =None,
        tinh_thanh_id =None,
        xa_phuong_id =None
        
    
        
    ):
        self.id = uuid.uuid4()
        self.so_giaychungnhan = so_giaychungnhan
        self.ngay_kiemtra = ngay_kiemtra
        self.ngay_cap = ngay_cap
        self.ngay_hieu_luc = ngay_hieu_luc
        self.ngay_het_han = ngay_het_han
        self.diachi = diachi
        self.dinhkem_giaychungnhan = dinhkem_giaychungnhan
        self.coso_kinhdoanh_id = coso_kinhdoanh_id
        self.trang_thai = trang_thai
        self.quan_huyen_id = quan_huyen_id
        self.tinh_thanh_id =tinh_thanh_id
        self.xa_phuong_id = xa_phuong_id
        
        
@event.listens_for(ChungNhanCoSo, "before_insert")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()


@event.listens_for(ChungNhanCoSo, "before_update")
def on_update_trigger(mapper, connection, target):
    target.updated_at = datetime.datetime.now()      
        
        
        
       
        # self.is_super_admin = is_super_admin
       


