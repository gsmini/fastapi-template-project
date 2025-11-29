from fastapi import APIRouter, Depends, HTTPException, Request

from src.libs._fastapi import make_ok_resp

router = APIRouter(
    prefix="/api/v1/celery",
    tags=["celery"],
    responses={404: {"description": "Not found"}},
)


@router.get("/create")  # curl http://0.0.0.0:8000/api/v1/celery/create
async def create_celery_task():
    # 防止循环引用
    from src.tasks import task_demo

    task_demo.delay("xxx")
    return make_ok_resp({"username": "admin"})
