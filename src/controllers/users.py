import json
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException, Request

from src.libs.fastapi_ import make_ok_resp
from src.libs.exceptions import InvalidParameter
from src.libs.logging import logger
from src.models.user import User

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
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
async def exception_user():
    # 模拟参数错误 通过raise exception返回
    logger.info("xxsdasd")
    raise InvalidParameter


class DataRequest(BaseModel):
    # data 为必填项，字符串类型，最小长度 2，最大长度 20
    username: str = Field(
        ...,  # ... 表示必填（无默认值）
        min_length=2,  # 最小长度 2
        max_length=20,  # 最大长度 20
        description="需要处理的字符串数据（必填，长度2-20之间）",
        examples=["hello", "pydantic"]  # 文档示例
    )
    # 可选：其他字段（如类型、分类等）
    password: str = Field(..., min_length=5, max_length=10, description="密码")


@router.post("/register")
async def register_user(request: Request):
    raw_json = await request.body()  # 获取原始字节流
    try:
        raw_json_dict = json.loads(raw_json.decode("utf-8"))  # 转换为字符串
        try:
            data = DataRequest(**raw_json_dict)
            ins = User.create(data.username, data.password)
            print(ins.to_dict())
            return make_ok_resp(data=ins.to_dict())
        except Exception as e:
            logger.info(f"register_user err:{e} request_id {getattr(request.state, 'request_id')}")
            raise InvalidParameter
    except Exception as e:
        logger.info(f"register_user err2{e}")
        raise InvalidParameter
