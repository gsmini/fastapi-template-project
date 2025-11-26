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

        # 3. 处理请求体（只解析 JSON 类型，兼容 GET/无请求体的情况）
        if "application/json" in request.headers.get("content-type", "").lower():
            try:
                # 解析 bytes 为 JSON（如果是 GET 或无请求体，body 为空，json() 会返回 {}）
                json_data = await request.json()
            except json.JSONDecodeError:
                # 非 JSON 格式的请求体（如语法错误），记录原始 bytes
                json_data = await request.body()
                logger.warning(f"[invalid json]| request_id: [{request_id}] | raw_body: [{json_data}]")
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
        if "application/json" in response.headers.get("Content-Type", "").lower() and request.method.lower() == "post":
            # 👉 关键：读取流式内容并缓存，同时生成新迭代器
            cached_chunks = []  # 缓存所有块

            # 1. 读取并缓存所有流式块（获取完整内容）
            full_content = b""
            async for chunk in response.body_iterator:
                cached_chunks.append(chunk)  # 缓存块，供新迭代器使用
                full_content += chunk  # 拼接完整内容

            # 2. 打印完整内容
            # Decode the bytes to a string for printing
            decoded_body = full_content.decode()
            print(f"Response Body: {decoded_body}")

            logger.info(
                f"[after request|request_id: {request_id}] data: {decoded_body}")

            return Response(content=full_content, status_code=response.status_code, headers=dict(response.headers),
                            media_type=response.media_type)

        return response
