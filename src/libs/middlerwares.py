import uuid
import json
from src.libs.logging import logger
from fastapi import FastAPI, Request
from starlette.responses import Response


def add_print_request_id_mid(app: FastAPI):
    @app.middleware("http")
    async def mid_print_request_id(request: Request, call_next):
        # 1. 放行 Swagger 相关路由（避免影响文档访问）
        swagger_paths = {"/docs", "/redoc", "/openapi.json", "/docs/oauth2-redirect"}
        if request.url.path in swagger_paths:
            response = await call_next(request)
            return response

        request_id = str(uuid.uuid4())
        request.state.request_id = request_id  # 存储到请求状态，供其他路由使用

        if "application/json" in request.headers.get("content-type", "").lower():
            try:
                # 解析 bytes 为 JSON（如果是 GET 或无请求体，body 为空，json() 会返回 {}）
                json_data = await request.json()
            except json.JSONDecodeError:
                # 非 JSON 格式的请求体（如语法错误），记录原始 bytes
                json_data = await request.body()
                logger.info(f"[invalid json]| request_id: [{request_id}] | raw_body: [{json_data}]")
        else:
            # 非 JSON 请求，记录请求参数（GET 用 query，POST 用 form 等）
            json_data = dict(request.query_params) if request.method == "GET" else "non-json request"

        # 4. 日志记录请求信息
        logger.info(
            f"[before request]| request_id: [{request_id}] | request_method: [{request.method}] "
            f"| request_path: [{request.url.path}] | request_data: [{json_data}]"
        )

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        # 6.2 （可选）JSON 响应体中添加 request_id（不影响非 JSON 响应）
        if "application/json" in response.headers.get("Content-Type", "").lower():

            # 1. 读取并缓存所有流式块（获取完整内容）
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk  # 拼接完整内容

            try:
                response_data = json.loads(response_body.decode())
                if isinstance(response_data, dict):
                    response_data["request_id"] = request_id
                    modified_response_body = json.dumps(response_data).encode()
                else:
                    modified_response_body = response_body  # Not a dict, don't modify
            except json.JSONDecodeError:
                logger.error("middleware process err: json decode err")
                modified_response_body = response_body  # Not JSON, don't modify

            new_response = Response(
                content=modified_response_body,
                status_code=response.status_code,
                headers=response.headers,
                media_type=response.media_type,

            )
            new_response.headers["content-length"] = str(len(modified_response_body))
            logger.info(
                f"[after request]| request_id: [ {request_id} ] | response_data: [ {json.loads(modified_response_body)} ]"
            )
            return new_response

        return response
