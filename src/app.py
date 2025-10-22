from src.controllers import init_routes
from src.libs.exceptions import APIException
from src.libs.logging import logger
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.libs.middlerwares import add_print_request_id_mid


def create_app():
    app = FastAPI(title="我的fastapi服务", debug=True)  # debug=True直接返回500错误信息
    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # 允许访问跳转的域名 一般写部署的地址域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(APIException)
    async def handle_error(request: Request, e: APIException):
        resp = {
            "code": e.error_code,
            "message": e.message,
            "data": {}
        }
        logger.error(f"[exception]|request_id:{request.headers.get('request_id')}|resp={resp}")
        return JSONResponse(content=resp, status_code=e.http_code)

    add_print_request_id_mid(app)
    init_routes(app)
    return app
