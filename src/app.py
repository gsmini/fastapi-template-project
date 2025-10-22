from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    app = FastAPI(title="我的fastapi服务", debug=True)

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
    return app
