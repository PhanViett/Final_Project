from flask_restful import Resource
from flask import request
from application.models.giay_phep_kinh_doanh import GiayPhepKinhDoanh

from application.utils.helper.string_processing_helper import clean_string



class GiayPhepKinhDoanhPublic(Resource):
    query = GiayPhepKinhDoanh.query

    ten_co_so = request.json.get('ten_co_so')
    so_giay_chung_nhan = request.json.get('so_giay_chung_nhan')
    quan_huyen = request.json.get('quan_huyen_id')
    xa_phuong = request.json.get('xa_phuong_id')
    ten_duoc_si = request.json.get('ten_duoc_si')
    so_cchnd = request.json.get('so_cchnd')
    gdp_gpp = request.json.get('quan_huyen')
    trang_thai = request.json.get('trang_thai')

    if ten_co_so is not None :

        query = query.filter(GiayPhepKinhDoanh.ten_coso_khongdau.like(f"%{clean_string(ten_co_so)}%"))

    if so_giay_chung_nhan is not None:

        query = query.filter(GiayPhepKinhDoanh.so_giay_phep.like(f"%{so_giay_chung_nhan}%"))

    if quan_huyen is not None:

        query = query.filter(GiayPhepKinhDoanh.quanhuyen_coso_id == quan_huyen)

    if xa_phuong is not None:

        query = query.filter(GiayPhepKinhDoanh.xaphuong_coso_id == xa_phuong)

    if ten_duoc_si is not None:

        query = query.filter(GiayPhepKinhDoanh.nguoi_tncm_ten.like(f"%{clean_string(ten_duoc_si)}%"))

    if so_cchnd is not None:

        query = query.filter(GiayPhepKinhDoanh.so_giay_phep.like(f"%{so_cchnd}%"))
    
    if gdp_gpp is not None:

        query = query.filter(GiayPhepKinhDoanh.so_giay_gps == gdp_gpp)