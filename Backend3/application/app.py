import os
from flask import Flask, request
from application.controllers import (
    nhan_vien,
    auth,
    records,
    vai_tro,
    location,
    tin_tuc
)

from application import manage
from application.utils.resource.http_code import HttpCode
from application.extensions import apispec
from application.extensions import db
from application.extensions import jwt
from application.extensions import migrate

from jwt import ExpiredSignatureError
from flask_cors import CORS
from flask_seeder import FlaskSeeder
# from elasticapm.contrib.flask import ElasticAPM


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("application")

    # apm = ElasticAPM(
    #     app,
    #     server_url=os.getenv("APM_SERVER_URL"),
    #     service_name=str("service-congsuckhoe-ip-version-build"),
    #     environment="dev",
    # )

    CORS(app, support_credentials=True)
    app.config.from_object("application.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    configure_cli(app)
    configure_apispec(app)
    register_blueprints(app)
    configure_token_error(app)


    @app.route("/")
    def default():
        return (
            str(os.getenv("FLASK_BUILD_VERSION"))
            + "<br /> - "
            + os.getenv("FLASK_BUILD_DATE")
            + "<br /> - Requester IP: "
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
    seeder = FlaskSeeder()
    seeder.init_app(app, db)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


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


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(nhan_vien.views.blueprint)
    app.register_blueprint(vai_tro.views.blueprint)
    app.register_blueprint(records.views.blueprint)
    app.register_blueprint(location.views.blueprint)
    app.register_blueprint(tin_tuc.views.blueprint)





