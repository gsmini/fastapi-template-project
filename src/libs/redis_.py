# -*- coding:utf-8 -*-

from src.config import REDIS_URI


def _get_redis_client():
    from redis import StrictRedis
    return StrictRedis.from_url(REDIS_URI, decode_responses=True)


rds = _get_redis_client()
if __name__ == "__main__":
    rds.set("a", "b", 10)
