from typing import Annotated
from fastapi import Request, HTTPException, Depends

from src.libs.logging import logger
from src.libs import exceptions
from src.libs.jwt_utils import decode_token
from src.models.user import User


# 仿造django一样给一个user对象
class RequestUser:
    username = ""
    email = ""
    user_id = 0
    is_stuff = 0
    is_superuser = 0


def user_login_required(request: Request):
    token = request.headers.get("Authorization")
    data = decode_token(token)
    logger.info(f"user_login_required jwt data:[{data}]")
    user = User.query_by_email(data.get("email", ""))
    if not user:
        raise exceptions.ExceptEmailNotExist
    wrap_user = RequestUser()
    wrap_user.username = data.get("username", "")
    wrap_user.email = data.get("email", "")
    wrap_user.user_id = data.get("user_id", 0)
    wrap_user.is_stuff = data.get("is_stuff", 0)
    wrap_user.is_superuser = data.get("is_superuser", 0)
    return wrap_user


UserLoginRequired = Annotated[bool, Depends(user_login_required)]


# 管理员
def stuff_user_login_required(request: Request):
    token = request.headers.get("Authorization")
    data = decode_token(token)
    logger.info(f"user_login_required jwt data:[{data}]")
    user = User.query_by_email(data.get("email", ""))
    if not user:
        raise exceptions.ExceptEmailNotExist

    if not user.is_stuff:
        raise exceptions.ExceptIsNotStuff

    current_user = RequestUser()
    current_user.username = data.get("username", "")
    current_user.email = data.get("email", "")
    current_user.user_id = data.get("user_id", 0)
    current_user.is_stuff = data.get("is_stuff", 0)
    current_user.is_superuser = data.get("is_superuser", 0)
    return current_user


StuffUserLoginRequired = Annotated[bool, Depends(stuff_user_login_required)]


# 超级管理员
def admin_user_login_required(request: Request):
    token = request.headers.get("Authorization")
    data = decode_token(token)
    logger.info(f"jwt decode data:[{data}]")
    user = User.query_by_email(data.get("email", ""))
    if not user:
        raise exceptions.ExceptEmailNotExist

    if not (user.is_stuff and user.is_superuser):
        raise exceptions.ExceptIsNotSuperuser
    current_user = RequestUser()
    current_user.username = data.get("username", "")
    current_user.email = data.get("email", "")
    current_user.user_id = data.get("user_id", 0)
    current_user.is_stuff = data.get("is_stuff", 0)
    current_user.is_superuser = data.get("is_superuser", 0)
    return current_user


AdminUserLoginRequired = Annotated[bool, Depends(admin_user_login_required)]
