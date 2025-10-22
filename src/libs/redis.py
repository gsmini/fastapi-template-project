# -*- coding:utf-8 -*-

from src.config import REDIS_URI


def _get_redis_client():
    if "/tmp/" in REDIS_URI:
        from redislite import Redis

        return Redis(REDIS_URI, decode_responses=True)
    else:
        from redis import StrictRedis

        return StrictRedis.from_url(REDIS_URI, decode_responses=True)


rds = _get_redis_client()
