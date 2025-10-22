from fastapi import APIRouter, Depends, HTTPException
from src.libs.fastapi_ import make_ok_resp

router = APIRouter(
    prefix="/api/v1/users",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def update_user():
    return make_ok_resp({"user": "gsmini"})
