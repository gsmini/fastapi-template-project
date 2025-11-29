from fastapi import APIRouter, Depends, HTTPException, Request
from src.libs.logging import logger


def get_request_id(request: Request):
    try:
        req_id = getattr(request.state, 'request_id', "")
        return req_id
    except Exception as e:
        logger.info(f"get request_id err: [ {e} ]")
        return ""
