from src.controllers import init_routes
from src.libs.exceptions import APIException
from src.libs.logging import logger
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.libs.middlerwares import add_print_request_id_mid
from src.config import SENTRY_DSN, DEBUG

import sentry_sdk


def create_app():
    app = FastAPI(title="我的fastapi服务", debug=DEBUG)  # debug=True直接返回500错误信息
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        sample_rate=1.0
    )

    @app.get("/sentry-debug")
    async def trigger_error():
        division_by_zero = 1 / 0

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

    init_routes(app)
    add_print_request_id_mid(app)

    return app
