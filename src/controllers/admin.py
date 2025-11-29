import json
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.exc import IntegrityError

from src.libs import exceptions
from src.libs.exceptions import InvalidParameter
from src.libs._fastapi import make_ok_resp
from src.libs.logging import logger

from src.libs.get_req_id import get_request_id
from src.libs.depends_ import StuffUserLoginRequired
from src.models.user import User

from src.models.user_feedback_type import UserFeedbackType
from src.models.user_feedback_record import UserFeedbackRecord, UserFeedbackRecordStatus


router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)


class APiUsersQueryParams(BaseModel):
    offset: int = Field(0, ge=0, description="页码，至少为0")  # 可选参数，默认0，最小值0
    limit: int = Field(10, ge=1, le=100, description="每页条数，1-100之间")  # 可选参数，默认10


@router.get("/users")
async def APiUsers(request: Request, req_user: StuffUserLoginRequired):
    query_dict = dict(request.query_params)
    # 将查询参数字典转换为 Pydantic 模型（自动验证）
    try:
        params = APiUsersQueryParams(**query_dict)
    except Exception as e:
        logger.info(f"admin list user err: {e} request_id {get_request_id(request)}")
        raise InvalidParameter
    data = User.paginate(params.limit, params.offset)
    return make_ok_resp(data=data)


class ApiUserFeedbackTypeListQueryParams(BaseModel):
    offset: int = Field(0, ge=0, description="页码，至少为0")  # 可选参数，默认0，最小值0
    limit: int = Field(10, ge=1, le=100, description="每页条数，1-100之间")  # 可选参数，默认10


@router.get("/feedback-type")
async def ApiUserFeedbackTypeList(request: Request, req_user: StuffUserLoginRequired):
    query_dict = dict(request.query_params)
    # 将查询参数字典转换为 Pydantic 模型（自动验证）
    try:
        req_params = ApiUserFeedbackTypeListQueryParams(**query_dict)
    except Exception as e:
        logger.info(f"api feedback-type err: {e} request_id {get_request_id(request)}")
        raise InvalidParameter
    data = UserFeedbackType.paginate(req_params.limit, req_params.offset)
    return make_ok_resp(data=data)


class ApiUserFeedbackTypeCreateReq(BaseModel):
    feedback_type: str = Field(
        ...,  # ... 表示必填（无默认值）
        min_length=2,  # 最小长度 2
        max_length=20,  # 最大长度 20
        description="需要处理的字符串数据（必填，长度2-20之间）"
    )

    desc: str = Field(
        ...,  # ... 表示必填（无默认值）
        min_length=2,  # 最小长度 2
        max_length=200,  # 最大长度 20
        description="需要处理的字符串数据（必填，长度2-20之间）"
    )
    feedback_reply: str = Field(..., min_length=0, max_length=1000, description="回复内容")


@router.post("/feedback-type")
async def ApiUserFeedbackTypeCreate(request: Request, req_user: StuffUserLoginRequired):
    raw_json = await request.body()  # 获取原始字节流
    try:
        raw_json_dict = json.loads(raw_json.decode("utf-8"))  # 转换为字符串
        req_data = ApiUserFeedbackTypeCreateReq(**raw_json_dict)
    except Exception as e:
        logger.info(f"register_user err:{e} request_id {get_request_id(request)}")
        raise exceptions.InvalidParameter
    ins = UserFeedbackType.query_by_(req_data.feedback_type)
    if ins:
        raise exceptions.ExceptFeedBackTypeExist

    update_data = {
        "feedback_type": req_data.feedback_type,
        "desc": req_data.desc,
        "feedback_reply": req_data.feedback_reply
    }
    try:
        UserFeedbackType.create(**update_data)
    except IntegrityError as e:
        logger.info(f"UserFeedbackType err:[e]")
        raise exceptions.ExceptFeedBackTypeExist
    return make_ok_resp(data={})


class ApiUserFeedbackTypeModifyReq(BaseModel):
    obj_id: int = Field(1, ge=0, description="数据id")
    feedback_type: str = Field(
        ...,  # ... 表示必填（无默认值）
        min_length=2,  # 最小长度 2
        max_length=20,  # 最大长度 20
        description="需要处理的字符串数据（必填，长度2-20之间）"
    )

    desc: str = Field(
        ...,  # ... 表示必填（无默认值）
        min_length=2,  # 最小长度 2
        max_length=200,  # 最大长度 20
        description="需要处理的字符串数据（必填，长度2-20之间）"
    )
    feedback_reply: str = Field(..., min_length=0, max_length=1000, description="回复内容")


@router.post("/feedback-type-update")
async def ApiUserFeedbackTypeModify(request: Request, req_user: StuffUserLoginRequired):
    raw_json = await request.body()  # 获取原始字节流
    try:
        raw_json_dict = json.loads(raw_json.decode("utf-8"))  # 转换为字符串
        req_data = ApiUserFeedbackTypeModifyReq(**raw_json_dict)
    except Exception as e:
        logger.info(f"register_user err:{e} request_id {get_request_id(request)}")
        raise exceptions.InvalidParameter

    ins = UserFeedbackType.query_by_id(req_data.obj_id)
    if not ins:
        raise exceptions.ExceptFeedBackTypeNotExist

    update_data = {
        "feedback_type": req_data.feedback_type,
        "desc": req_data.desc,
        "feedback_reply": req_data.feedback_reply
    }

    try:
        UserFeedbackType.update(req_data.obj_id, **update_data)

    except IntegrityError as e:
        logger.info(f"UserFeedbackType err:[e]")
        raise exceptions.ExceptFeedBackTypeExist
    return make_ok_resp(data={})


class ApiUserFeedbackTypeDelReq(BaseModel):
    obj_id: int = Field(1, ge=0, description="数据id")


@router.post("/feedback-type-del")
async def ApiUserFeedbackTypeDel(request: Request, req_user: StuffUserLoginRequired):
    raw_json = await request.body()  # 获取原始字节流
    try:
        raw_json_dict = json.loads(raw_json.decode("utf-8"))  # 转换为字符串
        req_data = ApiUserFeedbackTypeDelReq(**raw_json_dict)
    except Exception as e:
        logger.info(f"register_user err:{e} request_id {get_request_id(request)}")
        raise exceptions.InvalidParameter

    ins = UserFeedbackType.query_by_id(req_data.obj_id)
    if not ins:
        raise exceptions.ExceptFeedBackTypeNotExist

    update_data = {
        "delete_flag": 1,
    }
    UserFeedbackType.update(req_data.obj_id, **update_data)
    return make_ok_resp(data={})


class ApiUserFeedbackRecordParams(BaseModel):
    offset: int = Field(0, ge=0, description="页码，至少为0")  # 可选参数，默认0，最小值0
    limit: int = Field(10, ge=1, le=100, description="每页条数，1-100之间")  # 可选参数，默认10


@router.get("/feedback-record")
async def ApiUserFeedbackRecordList(request: Request, req_user: StuffUserLoginRequired):
    query_dict = dict(request.query_params)
    # 将查询参数字典转换为 Pydantic 模型（自动验证）
    try:
        req_params = ApiUserFeedbackRecordParams(**query_dict)
    except Exception as e:
        logger.info(f"api feedback-type err: {e} request_id {get_request_id(request)}")
        raise InvalidParameter
    data = UserFeedbackRecord.paginate(req_params.limit, req_params.offset)
    return make_ok_resp(data=data)


# 修改
class ApiUserFeedbackRecordUpdateReq(BaseModel):
    obj_id: int = Field(1, ge=0, description="数据id")
    feedback_reply: str = Field(..., min_length=0, max_length=1000, description="回复内容")


@router.post("/feedback-record-update")
async def ApiUserFeedbackRecordUpdate(request: Request, req_user: StuffUserLoginRequired):
    raw_json = await request.body()  # 获取原始字节流
    try:
        raw_json_dict = json.loads(raw_json.decode("utf-8"))  # 转换为字符串
        req_data = ApiUserFeedbackRecordUpdateReq(**raw_json_dict)
    except Exception as e:
        logger.info(f"register_user err:{e} request_id {get_request_id(request)}")
        raise exceptions.InvalidParameter

    update_data = {
        "feedback_reply": req_data.feedback_reply
    }
    ins = UserFeedbackRecord.update(req_data.obj_id, **update_data)
    if not ins:
        raise exceptions.ExceptFeedRecordTypeNotExist

    return make_ok_resp()


# 审核
class ApiUserFeedbackRecordApprovalReq(BaseModel):
    obj_id: int = Field(1, ge=0, description="数据id")
    status: int = Field(1, ge=0, description="数据id")


@router.post("/feedback-record-approval")
async def ApiUserFeedbackRecordApproval(request: Request, req_user: StuffUserLoginRequired):
    raw_json = await request.body()  # 获取原始字节流
    try:
        raw_json_dict = json.loads(raw_json.decode("utf-8"))  # 转换为字符串
        req_data = ApiUserFeedbackRecordApprovalReq(**raw_json_dict)
    except Exception as e:
        logger.info(f"register_user err:{e} request_id {get_request_id(request)}")
        raise exceptions.InvalidParameter

    update_data = {
        "status": req_data.status
    }
    ins = UserFeedbackRecord.update(req_data.obj_id, **update_data)
    if not ins:
        raise exceptions.ExceptFeedRecordTypeNotExist
    # 防止循环引用
    from src.tasks import task_demo
    if req_data.status == UserFeedbackRecordStatus.Approval:
        logger.info(f"审核数据成功{req_data.obj_id}")
        task_demo.delay(req_data.obj_id)

    return make_ok_resp()
