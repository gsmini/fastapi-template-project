# -*- coding:utf-8 -*-
import os
from dotenv import load_dotenv as _load_dotenv

_load_dotenv()

env = os.getenv

ENVIRONMENT = env("ENVIRONMENT", "dev")
DEBUG = False
EXPIRES_DELTA = 24 * 30  # 30天
# REDIS_URI
SENTRY_DSN = env("SENTRY_DSN", "")
SECRET_KEY = env("SECRET_KEY", "")
# REDIS_URI
REDIS_URI = env("REDIS_URI", "")  # REDIS_URI = "redis://xxxxx!@172.16.0.234:8635/0"
CELERY_BROKER_URI = env("REDIS_URI", "redis://:foobared@localhost:6379/2")

# MySQL配置
SQLALCHEMY_DATABASE_URI = env("SQLALCHEMY_DATABASE_URI",
                              "mysql+pymysql://root:e52ebe1f2e3bfdbae0da9@127.0.0.1:33306/fastapi_template_project")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = int(env("SQLALCHEMY_POOL_RECYCLE", 7200))
SQLALCHEMY_POOL_SIZE = int(env("SQLALCHEMY_POOL_SIZE", 100))
SQLALCHEMY_POOL_TIMEOUT = int(env("SQLALCHEMY_POOL_TIMEOUT", 180))
