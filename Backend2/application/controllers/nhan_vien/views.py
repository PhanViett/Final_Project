from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from application.extensions import apispec
from application.utils.resource.http_code import HttpCode
from application.controllers.nhan_vien.resources import (
    UserResource, UserList, UserInform, UserSearch,
    UserUnassignRole, UserAssignRole
)

from application.schemas import NhanVienSchema
from flask import Flask

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint, errors=Flask.errorhandler)


api.add_resource(UserResource, "/users/<user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")
api.add_resource(UserInform, "/profile", endpoint="profile")
api.add_resource(UserSearch, "/search", endpoint="search")
api.add_resource(UserUnassignRole, "/users/unassign/<id>")
api.add_resource(UserAssignRole, "/users/assign/<user_id>")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e: ValidationError):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return {
        'errorCode': "EC09",
        "msg": e.messages[next(iter(e.messages))][0]
    }, HttpCode.BadRequest
