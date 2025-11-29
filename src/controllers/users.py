import json
import random
from pydantic import BaseModel, Field
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Request


from src.libs import exceptions
from src.libs.logging import logger
from src.libs._fastapi import make_ok_resp
from src.libs.redis_ import rds
from src.libs.get_req_id import get_request_id
from src.libs.send_email import get_email_code_key
from src.libs.jwt_utils import generate_token
from src.libs.depends_ import UserLoginRequired, StuffUserLoginRequired

from src.models.user import User
from src.models.user_feedback_record import UserFeedbackRecord, UserFeedbackRecordStatus

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


class GetEmailCodeReq(BaseModel):
    email: str = Field(
        ...,  # ... 表示必填（无默认值）

        min_length=2,  # 最小长度 2
        max_length=20,  # 最大长度 20
        description="需要处理的字符串数据（必填，长度2-20之间）",
        examples=["hello", "pydantic"]  # 文档示例
    )
    email_type: Literal[1, 2, 3] = Field(
        ...,  # 表示必填字段（省略则为可选）
        description="状态值，仅支持 1、2、3"
    )


@router.post("/get-email-code")
async def get_email_code(request: Request):
    raw_json = await request.body()  # 获取原始字节流
    try:
        raw_json_dict = json.loads(raw_json.decode("utf-8"))  # 转换为字符串
        data = GetEmailCodeReq(**raw_json_dict)
    except Exception as e:
        logger.info(f"register_user err:{e} request_id {get_request_id(request)}")
        raise exceptions.InvalidParameter

    code = random.randint(100001, 999999)
    rds_key = get_email_code_key(data.email, data.email_type, code)
    rds.set(rds_key, code, 60 * 60)

    # 防止循环引用
    from src.tasks import task_email_send
    task_email_send.delay(get_request_id(request), data.email, code, data.email)
    return make_ok_resp(data={})


class RegisterReq(BaseModel):
    # data 为必填项，字符串类型，最小长度 2，最大长度 20
    username: str = Field(
        ...,  # ... 表示必填（无默认值）
        min_length=2,  # 最小长度 2
        max_length=20,  # 最大长度 20
        description="需要处理的字符串数据（必填，长度2-20之间）",
        examples=["hello", "pydantic"]  # 文档示例
    )
    email: str = Field(
        ...,  # ... 表示必填（无默认值）
        min_length=2,  # 最小长度 2
        max_length=20,  # 最大长度 20
        description="需要处理的字符串数据（必填，长度2-20之间）"
    )
    code: str = Field(
        ...,  # ... 表示必填（无默认值）
        min_length=6,  # 最小长度 2
        max_length=6,  # 最大长度 20
        description="需要处理的字符串数据（必填，长度2-20之间）"
    )
    # 可选：其他字段（如类型、分类等）
    password: str = Field(..., min_length=8, max_length=15, description="密码")


# 注册
@router.post("/register")
async def register(request: Request):
    raw_json = await request.body()  # 获取原始字节流
    try:
        raw_json_dict = json.loads(raw_json.decode("utf-8"))  # 转换为字符串
        data = RegisterReq(**raw_json_dict)
    except Exception as e:
        logger.info(f"register_user err:{e} request_id {get_request_id(request)}")
        raise exceptions.InvalidParameter

    if not rds.get(get_email_code_key(data.email, 1, data.code)):
        raise exceptions.ExceptEmailRdsCodeNotExist

    if User.query_by_username(data.username):
        raise exceptions.ExceptUsernameExist

    if User.query_by_email(data.email):
        raise exceptions.ExceptEmailExist

    ins = User.create(data.username, data.password, data.email)
    user_data = ins.to_dict()
    token = generate_token(
        payload=user_data,
    )
    user_data["token"] = token
    return make_ok_resp(data=user_data)


# 登陆
class LoginReq(BaseModel):
    email: str = Field(
        ...,  # ... 表示必填（无默认值）
        min_length=2,  # 最小长度 2
        max_length=20,  # 最大长度 20
        description="需要处理的字符串数据（必填，长度2-20之间）"
    )

    # 可选：其他字段（如类型、分类等）
    password: str = Field(..., min_length=8, max_length=15, description="密码")


@router.post("/login")
async def login(request: Request):
    raw_json = await request.body()  # 获取原始字节流
    try:
        raw_json_dict = json.loads(raw_json.decode("utf-8"))  # 转换为字符串
        data = LoginReq(**raw_json_dict)
    except Exception as e:
        logger.info(f"register_user err:{e} request_id {get_request_id(request)}")
        raise exceptions.InvalidParameter

    ins = User.query_by_email(data.email)
    if not ins:
        raise exceptions.ExceptEmailNotExist

    if not ins.verify_pwd(data.email, data.password):
        raise exceptions.ExceptPwdNotMatch

    user_data = ins.to_dict()
    token = generate_token(
        payload=user_data,
    )
    user_data["token"] = token
    return make_ok_resp(data=user_data)


# 查看我的信息
@router.get("/user-info")
async def userinfo(request: Request, req_user: UserLoginRequired):
    ins = User.query_by_email(req_user.email)
    if not ins:
        raise exceptions.ExceptEmailNotExist
    return make_ok_resp(data=ins.to_dict())


# faq新增反馈
class ApiUserFeedbackRecordCreateReq(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="需要处理的字符串数据（必填，长度2-20之间）"
    )

    feedback_type: str = Field(
        ...,  # ... 表示必填（无默认值）
        min_length=1,  # 最小长度 2
        max_length=20,  # 最大长度 20
        description="需要处理的字符串数据（必填，长度2-20之间）"
    )

    content: str = Field(
        ...,  # ... 表示必填（无默认值）
        min_length=1,  # 最小长度 2
        max_length=200,  # 最大长度 20
        description="需要处理的字符串数据（必填，长度2-20之间）"
    )


@router.post("/feedback-record")
async def ApiUserFeedbackRecordCreate(request: Request, req_user: StuffUserLoginRequired):
    raw_json = await request.body()  # 获取原始字节流
    try:
        raw_json_dict = json.loads(raw_json.decode("utf-8"))  # 转换为字符串
        req_data = ApiUserFeedbackRecordCreateReq(**raw_json_dict)
    except Exception as e:
        logger.info(f"register_user err:{e} request_id {get_request_id(request)}")
        raise exceptions.InvalidParameter

    update_data = {
        "user_id": req_user.user_id,
        "user_email": req_user.email,
        "title": req_data.title,
        "feedback_type": req_data.feedback_type,
        "feedback_type_llm": "",
        "content": req_data.content,
        "feedback_reply": "",
        "status": UserFeedbackRecordStatus.Pending
    }
    ins = UserFeedbackRecord.create(**update_data)

    # 防止循环引用
    logger.info(f"创建数据成功{ins.id}")
    from src.tasks import task_demo
    task_demo.delay(ins.id)
    return make_ok_resp(data={})
