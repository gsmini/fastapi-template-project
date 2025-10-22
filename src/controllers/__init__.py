# -*- coding:utf-8 -*-

from src.controllers import admin, users


def init_routes(app):
    # 注册子模块的路由到总模块
    app.include_router(users.router)
    app.include_router(admin.router)

    @app.get("/ping")
    def ping():
        return "pong"

    return app
