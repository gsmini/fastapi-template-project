import uuid
import json
from typing import AsyncGenerator, Any
from src.libs.logging import logger
from fastapi import FastAPI, Request, Response as FastAPIResponse
from starlette.responses import Response as StarletteResponse
from starlette.types import Message


def add_print_request_id_mid(app: FastAPI):
    @app.middleware("http")
    async def mid_print_request_id(request: Request, call_next):
        # 1. 放行 Swagger 相关路由（避免影响文档访问）
        swagger_paths = {"/docs", "/redoc", "/openapi.json", "/docs/oauth2-redirect"}
        if request.url.path in swagger_paths:
            response = await call_next(request)
            return response

        # 2. 生成唯一 Request-ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id  # 存储到请求状态，供其他路由使用

        # 3. 处理请求体（只解析 JSON 类型，兼容 GET/无请求体的情况）
        json_data = None
        content_type = request.headers.get("content-type", "").lower()
        if "application/json" in content_type:
            try:
                # 解析 bytes 为 JSON（如果是 GET 或无请求体，body 为空，json() 会返回 {}）
                json_data = await request.json()
            except json.JSONDecodeError:
                # 非 JSON 格式的请求体（如语法错误），记录原始 bytes
                json_data = await request.body()
                logger.warning(f"[invalid json]| request_id:[{request_id}] | raw_body:[{json_data}]")
        else:
            # 非 JSON 请求，记录请求参数（GET 用 query，POST 用 form 等）
            json_data = dict(request.query_params) if request.method == "GET" else "non-json request"

        # 4. 日志记录请求信息
        logger.info(
            f"[before request]| request_id:[{request_id}] | request_method:[{request.method}] "
            f"| request_path:[{request.url.path}] | request_data:[{json_data}]"
        )

        # 5. 传递请求到路由函数，获取响应
        response: StarletteResponse = await call_next(request)

        # 6. 给响应添加 Request-ID（响应头 +  JSON 响应体）
        # 6.1 响应头添加 X-Request-ID（推荐，不侵入响应体）
        response.headers["X-Request-ID"] = request_id

        # 6.2 （可选）JSON 响应体中添加 request_id（不影响非 JSON 响应）
        if "application/json" in response.headers.get("Content-Type", "").lower():
            # 处理普通 JSON 响应（非流式）
            if hasattr(response, "body"):
                try:
                    # 解析响应体 bytes 为 dict，添加 request_id 后重新序列化
                    response_body = json.loads(response.body)
                    if isinstance(response_body, dict):
                        response_body["request_id"] = request_id
                        # 更新响应体（需重新编码为 bytes）
                        response.body = json.dumps(response_body).encode("utf-8")
                        # 重新计算 Content-Length（因为响应体长度变化了）
                        response.headers["Content-Length"] = str(len(response.body))
                except (json.JSONDecodeError, TypeError):
                    # 响应体不是 JSON 格式（如字符串），不处理
                    pass

            # 处理流式 JSON 响应（如果需要支持）
            # if hasattr(response, "body_iterator") and response.body_iterator:
            #     response.body_iterator = wrap_streaming_response(response.body_iterator, request_id)
            #     # 流式响应移除 Content-Length（长度动态变化）
            #     response.headers.pop("Content-Length", None)

        # 7. 日志记录响应信息
        logger.info(
            f"[after response]| request_id:[{request_id}] | status_code:[{response.status_code}] "
            f"| content_type:[{response.headers.get('Content-Type')}]"
        )

        return response


# （可选）流式 JSON 响应包装器（如果需要支持流式响应体注入 request_id）
async def wrap_streaming_response(body_iterator: AsyncGenerator[bytes, None], request_id: str) -> AsyncGenerator[bytes, None]:
    first_chunk = True
    async for chunk in body_iterator:
        if first_chunk and chunk:
            try:
                # 假设流式响应是 JSON 数组或对象，这里简化处理（实际需根据格式调整）
                data = json.loads(chunk.decode("utf-8"))
                if isinstance(data, dict):
                    data["request_id"] = request_id
                chunk = json.dumps(data).encode("utf-8")
            except json.JSONDecodeError:
                pass
            first_chunk = False
        yield chunk