from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/api/v1/users",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def update_user():
    return {"message": "user"}
