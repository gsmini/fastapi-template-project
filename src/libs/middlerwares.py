import uuid
from typing import AsyncGenerator, Any
from src.libs.logging import logger
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import Response as BaseResponse


def wrap_streaming_response_print(original_iterator: AsyncGenerator[bytes, Any], request_id: str) -> AsyncGenerator[
    bytes, Any]:
    """
        处理流式响应：打印每块内容，并包装request_id
        就是似乎是因为fastapi的response 默认内部就是stream的 所以只能通过这种方式
    """

    async def wrapped_iterator():
        # 1. 输出JSON开头（包含request_id）
        start_chunk = f'{{"request_id": "{request_id}", "data": ['.encode("utf-8")
        logger.info(f"[流式响应块] request_id={request_id} | 内容: {start_chunk.decode('utf-8')}")  # 打印开头块
        yield start_chunk

        # 2. 迭代原始流式内容，逐块打印
        first_chunk = True
        async for chunk in original_iterator:
            # 解码为字符串（方便打印，非必需）
            chunk_str = chunk.decode("utf-8", errors="ignore")
            logger.info(f"[流式响应块] request_id={request_id} | 内容: {chunk_str}")

            # 处理分隔符并发送
            if not first_chunk:
                yield b", "
            yield chunk
            first_chunk = False

        # 3. 输出JSON结尾
        end_chunk = b"]}"
        logger.info(f"[流式响应块] request_id={request_id} | 内容: {end_chunk.decode('utf-8')}")  # 打印结尾块
        yield end_chunk

    return wrapped_iterator()


def add_print_request_id_mid(app):
    @app.middleware("http")
    async def mid_print_request_id(request: Request, call_next):
        # swagger相关路由直接放行，不做任何处理 不然访问在线文档会报错
        swagger_paths = {"/docs", "/redoc", "/openapi.json", "/docs/oauth2-redirect"}
        if request.url.path in swagger_paths:
            return await call_next(request)

        # 只是针对application/json的请求
        if "application/json" not in request.headers.get("content-type", "").lower():
            return Response

        request_id = str(uuid.uuid4())
        json_data = await request.json()
        request.state.request_id = request_id  # 存储到请求状态中 其他代码可以通过{getattr(request.state, 'request_id')}获取
        # print 请求输出
        logger.info(
            f"[before request]| request_id:[{request_id}] |request_method:[{request.method}] | request_path:[{request.url.path}] |request_json:[{json_data}]"
        )

        response: Response = await call_next(request)  # 传递请求到路由函数

        # ------------------------------
        # 3. 响应返回前：附加 request_id 到响应
        # ------------------------------
        # 方式 1：添加到响应头（推荐，不侵入响应体，兼容所有响应类型）
        response.headers["X-Request-ID"] = request_id
        # 方式 2： 处理 JSON 响应（添加 request_id 到响应体）
        # 4.1 对JSON响应自动注入（Content-Type为application/json）

        if "application/json" in response.headers.get("Content-Type", "").lower():
            if isinstance(response, BaseResponse):
                # 流式JSON响应：包装生成器
                response.body_iterator = wrap_streaming_response_print(
                    response.body_iterator, request_id
                )
                # 流式响应移除Content-Length（长度动态变化）
                del response.headers["Content-Length"]

        return response
