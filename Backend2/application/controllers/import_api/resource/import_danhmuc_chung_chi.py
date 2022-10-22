from datetime import datetime, timezone
from unicodedata import name
from flask_restful import Resource
from flask import request, send_file
import pandas as pd
import numpy as np
from time import sleep, strptime
from application.models.danhmuc_noi_tot_nghiep import NoiTotNghiep
from application.models.user import User
from application.schemas.chung_chi_hanh_nghe import ChungChiHanhNgheSchema
from application.models.chung_chi_hanh_nghe import ChungChiHanhNghe
from application.models.danhmuc_van_bang_chuyen_mon import VanBangChuyenMon
from application.schemas.bang_cap import BangCapSchema
from application.schemas.nhan_vien import NhanVienSchema
from application.utils.helper.string_processing_helper import clean_string
from application.utils.resource.http_code import HttpCode
from application.extensions import db, redisdb

class ImportUserResource(Resource):
    def post(self):
        target_file = request.files.get("file",None)
        
        # if not target_file:
        #     return {
        #         "msg":"Missing file"
        #     }, HttpCode.BadRequest
        print("\033[1m\033[95m\033[94m"+"STARTING THE IMPORT PROCESS: READING EXCEL DATA"+"\033[0m")

        SHEET_NAME = "QuocTich"
        x = pd.read_excel(target_file,skiprows=1)
        x.replace(np.nan, None,inplace=True)
        x.rename(columns=
                 {
            "IDMAP":"id_mapping",
            "HO":"ho","TEN":"ten", "GIOITINH":"gioi_tinh",
            "NGAYTHANGNAMSINH":"ngay_sinh", 
            "CMND":"ma_cong_dan", "NGCAPCMND":"ngay_cap", "NOICAPCMND":"noi_cap",
            "DIACHI":"dia_chi", "SODT":"dien_thoai", "EMAIL":"email", "NOIOHIENNAY":"dia_chi_thuong_tru",
            "VANBANG":"ten_van_bang", "NAMCAPBANG":"nam_cap_bang","NOICAPBANG":"noi_cap_bang",
            "SOCCHN":"so_giay_phep","NGCAPCCHN":"ngay_cap_chung_chi", "NOICAPCCHN":"noi_cap_chung_chi",
            "GHICHU":"ghi_chu","GHICHUPHAMVI(CCHN)":"ghi_chu_pham_vi_hanh_nghe","GHICHUVITRI(CCHN)":"ghi_chu_vi_tri_hanh_nghe"
            },inplace=True)
        print("\033[1m\033[92m\033[94m"+"FINISHED READING EXCEL"+"\033[0m")
        print("\033[1m\033[95m\033[94m"+"START IMPORTING DATA"+"\033[0m")

        LOG = []
        total_fail = 0
        total_success = 0
        van_bang_list = {x.ten_khong_dau:str(x.id) for x in VanBangChuyenMon.query.all()}
        noi_cap_bang_list = {x.ten_khong_dau:str(x.id) for x in NoiTotNghiep.query.all()}
        sleep(1)
        
        
        for counter, item in enumerate(x.to_dict("records")):
            try:

                print("\033[1m\033[96m\033[94m"+"Process data"+"\033[0m")
                if pd.isnull(item["ngay_cap"]):
                    item["ngay_cap"] = None
                    print("\033[93m"+"ngay_cap propterty is Empty"+"\033[0m")
                if pd.isnull(item["ngay_sinh"]):
                    item["ngay_sinh"] = None
                    print("\033[93m"+"ngay_cap propterty is Empty"+"\033[0m")
                if pd.isnull(item["ngay_cap_chung_chi"]):
                    item["ngay_cap_chung_chi"] = None
                    print("\033[93m"+"ngay_cap_chung_chi propterty is Empty"+"\033[0m")
                if item["ngay_sinh"]:
                    try:
                        item["ngay_sinh"] = int(item["ngay_sinh"].timestamp())
                    except:
                        raise Exception("Ngày sinh không hợp lệ")    
                if item["ngay_cap"]:
                    try:
                        item["nam_cap"] = str(item["ngay_cap"].year)
                        item["ngay_cap"] = int(item["ngay_cap"].timestamp())
                    except:
                        raise Exception("Ngày cấp chứng minh nhân dân không hợp lệ")    
                if item["ngay_cap_chung_chi"]:
                    try:
                        item["ngay_cap_chung_chi"] = int(item["ngay_cap_chung_chi"].timestamp())
                    except:
                        raise Exception("Ngày cấp chứng chỉ không hợp lệ")
                if item["nam_cap_bang"]:
                    item["nam_cap_bang"] = str(int(item["nam_cap_bang"]))
                if item["noi_cap_bang"]:
                    target_noi_tot_nghiep = noi_cap_bang_list.get(process_string_noi_tot_nghiep(item["noi_cap_bang"]),None)
                else:target_noi_tot_nghiep=None
                if item["ten_van_bang"]:
                    target_van_bang = van_bang_list.get(clean_string(item["ten_van_bang"]),None)
                else: target_van_bang=None
                del item["ten_van_bang"]
                if item["id_mapping"]:
                    item["id_mapping"] = str(item["id_mapping"])
                if item["ma_cong_dan"]:
                    item["ma_cong_dan"] = process_numeric_or_string(item["ma_cong_dan"])
                    
                print("\033[1m\033[96m\033[94m"+"Creating nhan_vien"+"\033[0m")

                nhan_vien_data = {
                    "id_mapping": item["id_mapping"],
                    "ho":item["ho"],
                    "ten":item["ten"],
                    "ngay_sinh":item["ngay_sinh"],
                    "gioi_tinh":item["gioi_tinh"],
                    "ma_cong_dan":item["ma_cong_dan"],
                    "ngay_cap":item["ngay_cap"],
                    "noi_cap":item["noi_cap"],
                    "dia_chi":item["dia_chi"],
                    "dien_thoai":str(item["dien_thoai"]),
                    "email":item["email"],
                    "dia_chi_thuong_tru":item["dia_chi_thuong_tru"]
                }
                    
                schema = NhanVienSchema()
                created_nhan_vien: User = schema.load(nhan_vien_data)
                db.session.add(created_nhan_vien)
                db.session.flush()
                
                print("\033[1m\033[96m\033[94m"+"Creating bang_cap"+"\033[0m")

                if target_van_bang:
                    bang_cap_data = {
                        "nhan_vien_id": created_nhan_vien.id,
                        "van_bang_chuyen_mon_id":target_van_bang,
                        "nam_cap":str(item["nam_cap_bang"]),
                        "noi_tot_nghiep_id":target_noi_tot_nghiep,
                    }
                    created_bang_cap = BangCapSchema().load(bang_cap_data)
                    db.session.add(created_bang_cap)
                    db.session.flush()
                    
                print("\033[1m\033[96m\033[94m"+"Creating chung_chi"+"\033[0m")

                chung_chi_data = {
                    "nhan_vien_id": created_nhan_vien.id,
                    "van_bang_chuyen_mon_id": target_van_bang,
                    "co_quan_cap":item["noi_cap_chung_chi"],
                    "ngay_cap":item["ngay_cap_chung_chi"],
                    "so_giay_phep":item["so_giay_phep"],
                    "ghi_chu":item["ghi_chu"],
                    "ghi_chu_pham_vi_hanh_nghe":item["ghi_chu_pham_vi_hanh_nghe"],
                    "ghi_chu_vi_tri_hanh_nghe":item["ghi_chu_vi_tri_hanh_nghe"],
                    "nam_cap": item["nam_cap"] if item.get("nam_cap") else None
                }
                created_chung_chi = ChungChiHanhNgheSchema().load(chung_chi_data)
                db.session.add(created_chung_chi)
                db.session.commit()
                print("\033[1m\033[96m\033[94m"+"Import success"+"\033[0m")
                print("Mapping: {}, total_success: {}, total_failure: {}".format(item["id_mapping"],total_success,total_fail))

                total_success += 1
            except Exception as e:
                total_fail += 1
                print("\033[91m"+"Import failed")
                print("MESSAGE: "+e.args[0])
                print(item)
                print("\033[0m")
                item["ngay_sinh"] = str(item["ngay_sinh"])
                item["ngay_cap"] = str(item["ngay_cap"])
                item["ngay_cap_chung_chi"] = str(item["ngay_cap_chung_chi"])
                LOG.append({"id":item["id_mapping"], "message":e.args[0],"data":item})
                continue
        return {
            "msg":"Thanh cong",
            "results":{
                "total_fail":total_fail,
                "total_success":total_success,
                "log": LOG
            }
        }
        # return excel.make_response_from_records(array= x_list,file_type="xlsx",file_name="problem_data.csv")
     
     
def process_string_noi_tot_nghiep(ten_noi_tot_nghiep: str) -> str:
    ten_noi_tot_nghiep = clean_string(ten_noi_tot_nghiep, False)
    if "dai hoc" in ten_noi_tot_nghiep:
        list_of_words = ten_noi_tot_nghiep.split()
        if "truong" in list_of_words:
            list_of_words.remove("truong")
            ten_noi_tot_nghiep= " ".join(list_of_words)
    return ten_noi_tot_nghiep

def process_numeric_or_string(input) -> str:
    if isinstance(input,str):
        return input
    elif isinstance(input, float):
        return str(int(input))
    else:
        return None
    