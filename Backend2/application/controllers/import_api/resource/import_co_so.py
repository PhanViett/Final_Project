from datetime import datetime, timezone
from flask_restful import Resource
from flask import request, send_file
import pandas as pd
import numpy as np
from time import sleep, strptime
from application.models.co_so_kinh_doanh import CoSoKinhDoanh
from application.models import QuanHuyen, XaPhuong
from application.models.danhmuc_loai_hinh_kinh_doanh import LoaiHinhKinhDoanh
from application.models.danhmuc_van_bang_chuyen_mon import VanBangChuyenMon
from application.models.giay_phep_kinh_doanh import GiayPhepKinhDoanh
from application.utils.resource.http_code import HttpCode
from application.extensions import db, redisdb
import flask_excel as excel
from application.schemas.co_so_kinh_doanh import CoSoKinhDoanhSchema
from application.schemas.giay_phep_kinh_doanh import GiayPhepKinhDoanhSchema

class ImportCoSoesource(Resource):
    def post(self):
        target_file = request.files.get("file",None)
        
        # if not target_file:
        #     return {
        #         "msg":"Missing file"
        #     }, HttpCode.BadRequest
            
        SHEET_NAME = "QuocTich"
        print("\033[1m\033[95m\033[94m"+"STARTING THE IMPORT PROCESS: READING EXCEL DATA"+"\033[0m")
        x = pd.read_excel(target_file,skiprows=1)

        x.rename(columns=
                 {
                "IDMAP":"id_mapping",
                "TENCOSO":"ten_coso",
                "Email":"email_coso",
                "SODT":"dienthoai_coso",
                "SONHA":"so_nha_co_so",
                "DUONG":"duong_co_so",
                "PHUONG_ID":"ma_phuong",
                "QUAN_ID":"ma_quan",
                "SODDK":"so_giay_phep",
                "NGCAPDDK":"ngay_cap",
                "TENTRUSO":"ten_tru_so",
                "DIACHITRUSO":"dia_chi_tru_so",
                "GHICHU":"ghi_chu",
                "LOAIHINHHN":"ghi_chu_loai_hinh_kd",
                "PHAMVIHN":"ghi_chu_pham_vi_kd",
                "TENHTTCKD":"ten_httckd"
            },inplace=True)
        x.fillna(np.nan, inplace=True)
        x.replace(np.nan, None,inplace=True)
        x = x.replace({np.datetime64('NaT'):None})

        LOG = []
        list_of_existed_items = db.session.query(CoSoKinhDoanh.id_mapping).all()
        quan_huyen_data: list[QuanHuyen] = QuanHuyen.query.all()
        list_of_quan_huyen = {x.ma: str(x.id) for x in quan_huyen_data}
        
        xa_phuong_data: list[XaPhuong] = XaPhuong.query.all()
        list_of_xa_phuong = {x.ma: str(x.id) for x in xa_phuong_data}
        
        for counter, item in enumerate(x.to_dict("records")):
            try:
                # if item["id_mapping"] not in [777,1812,2974,3460,4936,6158,8033,8303,9217,17319]:
                #     continue
                if pd.isnull(item["ngay_cap"]):
                    item["ngay_cap"] = None
                    print("\033[93m"+"ngay_cap propterty is Empty")
                if str(item["id_mapping"]) in list_of_existed_items:
                    print("\033[93m"+"id_mapping exist")
                    raise Exception(item["id_mapping"] + " đã tồn tại")
                if item.get("ngay_cap",None):
                    item["ngay_cap"] = int(item["ngay_cap"].timestamp())
                else: item["ngay_cap"] = None
                print("\033[1m"+"Creating co_so_hanh_nghe...")
                co_so_data = {
                     "id_mapping":str(item["id_mapping"]),
                    "ten_coso":item["ten_coso"],
                    "email_coso":item["email_coso"],
                    "dienthoai_coso":item["dienthoai_coso"],
                    "diachi_coso": " ".join(list(filter(lambda x: x is not None ,[str(item["so_nha_co_so"]),str(item["duong_co_so"])]))),
                    "quan_huyen_id":list_of_quan_huyen[str(int(item["ma_quan"]))] if item.get("ma_quan",None) else None,
                    "xa_phuong_id":list_of_xa_phuong[str(int(item["ma_phuong"]))] if item.get("ma_phuong",None) else None
                }
                co_so:CoSoKinhDoanh= CoSoKinhDoanhSchema().load(co_so_data)
                db.session.add(co_so)
                db.session.flush()
                print("\033[1m"+"co_so_hanh_nghe created")
                print("\033[1m"+"Creating giay_phep_hanh_nghe...")

                giay_phep_data = {
                    "so_giay_phep":item["so_giay_phep"],
                    "ngay_cap":item["ngay_cap"],
                    "ten_tru_so":item["ten_tru_so"],
                    "dia_chi_tru_so":item["dia_chi_tru_so"],
                    "ghi_chu":item["ghi_chu"],
                    "ghi_chu_loai_hinh_kd":item["ghi_chu_loai_hinh_kd"],
                    "ghi_chu_pham_vi_kd":item["ghi_chu_pham_vi_kd"],
                    "ten_httckd":item["ten_httckd"]
                }
                giay_phep:GiayPhepKinhDoanh= GiayPhepKinhDoanhSchema().load(giay_phep_data)
                giay_phep.co_so_kinh_doanh_id = co_so.id
                db.session.add(giay_phep)
                db.session.flush()
                print("\033[1m"+"co_so_hanh_nghe created")
                print(co_so_data)
                print("---------------------------")
                print("\033[92m"+"SUCCESS")
                print(giay_phep_data)
                db.session.commit()
                sleep(0.2)
            except Exception as e:
                LOG.append({"id":item["id_mapping"], "message":e.args[0],"data":item})
                print("\033[91m" +"FAILED")
                print("\033[93m"+"\033[1m"+"\033[4m"+"Reason: "+e.args[0])
                print({"id":item["id_mapping"], "message":e.args[0],"data":item})
                continue
        return {
            "msg":"thanh cong",
            "result":LOG
        }
        # return excel.make_response_from_records(array= x_list,file_type="xlsx",file_name="problem_data.csv")
     