from fastapi import APIRouter, Depends, HTTPException
from src.libs.fastapi_ import make_ok_resp
from src.libs.exceptions import InvalidParameter

router = APIRouter(
    prefix="/api/v1/users",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def update_user():
    return make_ok_resp({"user": "gsmini"})


"""
# http://0.0.0.0:8000/api/v1/users/exception
{
    "code": 40002,
    "message": "Invalid parameter",
    "data": {}
}
"""


@router.post("/exception")
async def update_user():
    # 模拟参数错误 通过raise exception返回
    raise InvalidParameter
