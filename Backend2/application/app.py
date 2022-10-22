from flask import Flask
from application.controllers import (
    nhan_vien,
    auth,
    thong_bao,
    vai_tro

)
from application import manage
from application.controllers.danh_muc import loai_hinh_kinh_doanh
from application.controllers.danh_muc import noi_tot_nghiep
from application.controllers.danh_muc import vi_tri_hanh_nghe
from application.controllers.danh_muc import van_bang_chuyen_mon
from application.controllers.danh_muc import pham_vi_hoat_dong_kinh_doanh

from application.controllers.danh_muc import location
from application.controllers.danh_muc import hoi_dong
from application.controllers.danh_muc import hoat_dong_chuyen_mon
from application.controllers.danh_muc import thu_tuc
from application.controllers.danh_muc import chung_nhan_thuc_hanh_co_so
from application.controllers.danh_muc import thanh_phan_ho_so
from application.controllers import danh_sach_filter_condition
from application.controllers import co_so_kinh_doanh
from application.controllers import gps
from application.controllers import import_api
from application.controllers import loai_ma_chung_chi
from application.controllers import in_ho_so


from application.controllers.duoc_si import bang_cap, co_so_thuc_hanh, dao_tao, chung_chi_hanh_nghe, duoc_si_co_so,  yeu_cau_chung_chi_hanh_nghe, duoc_si_co_so_chua_giay_phep, lich_su_chung_chi
from application.controllers.co_so import yeu_cau_dang_ky_kinh_doanh, giay_phep_kinh_doanh
from application.controllers.to_chuc import noi_dung_thuc_hanh
from application.controllers.nhan_vien import quan_ly_nguoi_dung

from application.utils.resource.http_code import HttpCode
from application.extensions import apispec, migrate, jwt, db
from flask_restful import Api
# from application.extensions import celery
from jwt import ExpiredSignatureError
from flask_cors import CORS
import os
from jwt.exceptions import InvalidTokenError, DecodeError

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("application")

    CORS(app)
    app.config.from_object("application.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    configure_token_error(app)
    configure_cli(app)
    register_blueprints(app)
    # init_celery(app)

    # if app.debug == False:
    #     sentry_sdk.init(
    #         dsn="https://b613a1de4c294f4c870e15de8ddad308@o1336337.ingest.sentry.io/6618383",
    #         integrations=[FlaskIntegration()],
    #         traces_sample_rate=1.0,
    #     )

    @app.route("/")
    def default():
        import datetime
        LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        return (
            str(os.getenv("FLASK_BUILD_VERSION"))
            + "<br /> - "
            + os.getenv("FLASK_BUILD_DATE")
            + "<br /> - Requester IP: "
            + "<br /> - "
            + str(LOCAL_TIMEZONE.tzname)
        )

    @app.route("/debug-sentry")
    def trigger_error():
        division_by_zero = 1 / 0

    return app


def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)


def configure_token_error(app):

    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_error(e):
        return {"msg": "Hết hạn Token"}, HttpCode.UnAuthorized

    @jwt.unauthorized_loader
    def handle_unauthorized_error(e):
        return {"msg": "Thiếu Token"}, HttpCode.UnAuthorized

    @jwt.invalid_token_loader
    def handle_invalid_error(e):
        return {"msg": "Sai định dạng Token"}, HttpCode.UnAuthorized

    @app.errorhandler(InvalidTokenError)
    def handle_expired_error(e):
        return {"msg": "Sai định dạng Token"}, HttpCode.UnAuthorized

    @app.errorhandler(DecodeError)
    def handle_expired_error(e):
        return {"msg": "Sai định dạng Token"}, HttpCode.UnAuthorized


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(nhan_vien.views.blueprint)
    app.register_blueprint(loai_hinh_kinh_doanh.views.blueprint)
    app.register_blueprint(noi_tot_nghiep.views.blueprint)
    app.register_blueprint(vi_tri_hanh_nghe.views.blueprint)
    app.register_blueprint(van_bang_chuyen_mon.views.blueprint)
    app.register_blueprint(vai_tro.views.blueprint)
    app.register_blueprint(bang_cap.views.blueprint)
    app.register_blueprint(dao_tao.views.blueprint)
    app.register_blueprint(hoat_dong_chuyen_mon.views.blueprint)
    app.register_blueprint(pham_vi_hoat_dong_kinh_doanh.views.blueprint)
    app.register_blueprint(thu_tuc.views.blueprint)
    app.register_blueprint(hoi_dong.views.blueprint)
    app.register_blueprint(chung_chi_hanh_nghe.views.blueprint)
    app.register_blueprint(thong_bao.views.blueprint)
    app.register_blueprint(yeu_cau_chung_chi_hanh_nghe.views.blueprint)
    app.register_blueprint(co_so_kinh_doanh.views.blueprint)
    app.register_blueprint(chung_nhan_thuc_hanh_co_so.views.blueprint)
    app.register_blueprint(duoc_si_co_so.views.blueprint)
    app.register_blueprint(duoc_si_co_so_chua_giay_phep.views.blueprint)
    app.register_blueprint(yeu_cau_dang_ky_kinh_doanh.views.blueprint)
    app.register_blueprint(lich_su_chung_chi.views.blueprint)
    app.register_blueprint(danh_sach_filter_condition.views.blueprint)
    app.register_blueprint(gps.views.blueprint)
    app.register_blueprint(location.views.blueprint)
    app.register_blueprint(import_api.views.blueprint)
    app.register_blueprint(loai_ma_chung_chi.views.blueprint)
    app.register_blueprint(co_so_thuc_hanh.views.blueprint)
    app.register_blueprint(thanh_phan_ho_so.views.blueprint)
    app.register_blueprint(giay_phep_kinh_doanh.views.blueprint)
    app.register_blueprint(noi_dung_thuc_hanh.views.blueprint)
    app.register_blueprint(quan_ly_nguoi_dung.views.blueprint)
    app.register_blueprint(in_ho_so.views.blueprint)


# def init_celery(app=None):
#     app = app or create_app()
#     celery.conf.update(app.config.get("CELERY", {}))

#     class ContextTask(celery.Task):
#         """Make celery tasks work with Flask app context"""

#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery
