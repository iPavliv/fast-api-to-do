import uvicorn
from fastapi import FastAPI

from routers.task_lists_router import LIST_ROUTER
from routers.tasks_router import TASK_ROUTER

APP = FastAPI()
APP.include_router(TASK_ROUTER)
APP.include_router(LIST_ROUTER)


if __name__ == "__main__":
    uvicorn.run(APP)
