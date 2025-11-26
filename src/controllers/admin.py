import json
from fastapi import APIRouter, Depends, HTTPException, Request

from src.libs.exceptions import InvalidParameter
from src.libs.fastapi_ import make_ok_resp
from pydantic import BaseModel, Field

from src.libs.logging import logger
from src.models.user import User

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")  # http://0.0.0.0:8000/api/v1/admin
async def update_admin():
    return make_ok_resp({"username": "admin"})


# 定义查询参数的 Pydantic 模型
class QueryParams(BaseModel):
    offset: int = Field(0, ge=0, description="偏移量")  # 可选参数，默认0 也就是不分页
    limit: int = Field(10, ge=1, le=100, description="每页条数，1-100之间")  # 可选参数，默认10


"""
 curl http://0.0.0.0:8000/api/v1/admin/users
"""


@router.get("/users")
async def AdminUsers(request: Request):
    query_dict = dict(request.query_params)

    # 将查询参数字典转换为 Pydantic 模型（自动验证）
    try:
        params = QueryParams(**query_dict)
        data = User.paginate(params.limit, params.offset)
        return make_ok_resp(data=data)
    except Exception as e:
        logger.info(f"admin list user err :{e} request_id {getattr(request.state, 'request_id')}")
        raise InvalidParameter
