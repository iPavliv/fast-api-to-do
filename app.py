import uvicorn
from fastapi import FastAPI
from routers.tasks_router import ROUTER

APP = FastAPI()
APP.include_router(ROUTER)


if __name__ == "__main__":
    uvicorn.run(APP)
