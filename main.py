# -*- coding:utf-8 -*-
import os
import uvicorn

from src.app import create_app
from src.config import DEBUG

app = create_app()

if __name__ == "__main__":
    if DEBUG:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, workers=os.cpu_count() + 1)
