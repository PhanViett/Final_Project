from logging.handlers import BufferingHandler

from sqlalchemy import and_, update
from application.extensions import db
from application.models.so_thu_tu import SoThuTu


def generate_number(type, begin=1):
    check = db.session.query(SoThuTu).filter(SoThuTu.loai == type).first()
    if check is None:
        model = SoThuTu()
        model.loai = type
        model.so_thu_tu = begin
        db.session.add(model)
        db.session.commit()
        return 1
    model = update(SoThuTu).returning(SoThuTu.so_thu_tu).where(and_(SoThuTu.loai == type)).values(so_thu_tu= (SoThuTu.so_thu_tu +1))
    result = db.session.execute(model)
    db.session.commit()
    for row in result:
        return row[0]
