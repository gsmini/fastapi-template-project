from fastapi import APIRouter, Depends, HTTPException
from src.libs.fastapi_ import make_ok_resp

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")  # http://0.0.0.0:8000/api/v1/admin
async def update_admin():
    return make_ok_resp({"username": "admin"})
