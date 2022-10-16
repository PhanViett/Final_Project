
import json
from typing import List
import functools
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import current_user
from application.models.vai_tro import VaiTro
from application.models.user import User
from application.utils.resource.http_code import HttpCode


def convert_to_permission(list_of_permissions_value: List[str]) -> list:

    permissions_list: list = json.load(open('application/permissions.json', encoding='utf-8'))
    if len(list_of_permissions_value) <= 0:
        return permissions_list
    category_to_update_index: int = -1
    latest_category_value: str = None
    for value in list_of_permissions_value:
        category_value = value.split('.')[0]

        # DYNAMIC PROGRAMMING
        if latest_category_value != category_value:
            latest_category_value = category_value
            for category in permissions_list:
                if category["value"] == category_value:
                    category_to_update_index = permissions_list.index(category)
                    break

        # CHECK FOR PERMISSIONS TO UPDATE
        for permission in permissions_list[category_to_update_index]["children"]:
            if permission["value"] == value:
                permission["checked"] = True
    return permissions_list


def permissions_required(permission_field: str, permission_names: List[str] = None):
    def wrapper(fn):
        @functools.wraps(fn)
        def decorator(*args, **kwargs):

            # VALID THAT JWT EXIST
            verify_jwt_in_request()

            # GET THE CURRENT USER
            user: User = current_user

            # IF USER IS A SUPER ADMIN THEN PERMIT ALL REQUEST
            if user.is_super_admin == True:
                return fn(*args, **kwargs)
            # LOOP THROUGH CURRENT USER ROLES
            if not user.assigned_role:
                return {"msg": "Không có quyền truy cập"}, HttpCode.PermissionDenied

            PERMITTED = True  # DEFAULT PERMITTED BEFORE VALIDATION

            role: VaiTro = user.assigned_role

            # TURN permissions AS JSON INTO Dictionary
            permission_category_list = json.loads(role.vai_tro)

            permission_list: list = None
            for permission_cate in permission_category_list:
                if(permission_cate["value"] == permission_field):
                    permission_list = permission_cate["children"]
                    break

            # RETURN ERROR WHEN permission_field DOESN'T EXIST IN THE USER ROLES
            if not permission_list:
                PERMITTED = False

            # LOOP THROUGH THE DEMANDED PERMISSIONS
            for required_permission in permission_names:
                for user_permission in permission_list:
                    if not user_permission["value"] == f"{permission_field}.{required_permission}":
                        PERMITTED = False
                        continue
                    if not user_permission["checked"]:
                        PERMITTED = False
                        continue
                    else:
                        PERMITTED = True
                        break

            if PERMITTED == True:
                return fn(*args, **kwargs)

            return {"msg": "Không có quyền truy cập"}, HttpCode.PermissionDenied
        return decorator
    return wrapper


def get_user_permissions(nhan_vien: User):
    allowed_permissions = {}
    target_role: VaiTro = nhan_vien.assigned_role
    if not target_role:
        return None
    perm_tree = json.loads(target_role.vai_tro)
    for perm_cate in perm_tree:
        allowed_permissions[perm_cate["value"]] = {perm["type"]: perm["checked"]
                                                   for perm in perm_cate["children"]}

    return allowed_permissions
