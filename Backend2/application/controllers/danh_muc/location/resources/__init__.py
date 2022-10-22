# from application.controllers.danh_muc.location.resources.location import GetTinhThanh,TinhThanhById
from .tinh_thanh import TinhThanhCreate, TinhThanhGetAll, TinhThanhGetPaginate, TinhThanhUpdateDelete
from .quan_huyen import QuanHuyenCreate, QuanHuyenGetAll, QuanHuyenUpdateDelete, QuanHuyenGetPaginate
from .xa_phuong import XaPhuongCreate, XaPhuongGetAll, XaPhuongGetPaginate, XaPhuongUpdateDelete
__all__ = ["GetTinhThanh","TinhThanhById"]
