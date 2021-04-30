from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException

from fastapi_utils.api_model import APIMessage
from fastapi_utils.cbv import cbv

from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.status import HTTP_404_NOT_FOUND

from models import Task
from schemas import TODOCreate, TODOUpdate


SQLALCHEMY_DATABASE_URL = "sqlite:///todos.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

APP = FastAPI()
ROUTER = InferringRouter()


def get_task(task_id: int) -> Task:
    task: Optional[Task] = session.query(Task).get(task_id)
    if not task:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return task


@cbv(ROUTER)
class TaskView:
    @ROUTER.post("/task/add")
    def create_item(self, task: TODOCreate) -> TODOUpdate:
        task_orm = Task(desc=task.desc)
        session.add(task_orm)
        session.commit()
        return TODOUpdate.from_orm(task_orm)

    @ROUTER.get("/task/{task_id}")
    def read_item(self, task_id: int) -> TODOUpdate:
        task_orm = get_task(task_id)
        return TODOUpdate.from_orm(task_orm)

    @ROUTER.put("/task/{task_id}")
    def update_item(self, task_id: int, task: TODOCreate) -> TODOUpdate:
        task_orm = get_task(task_id)
        task_orm.desc = task.desc
        session.add(task_orm)
        session.commit()
        return TODOUpdate.from_orm(task_orm)

    @ROUTER.delete("/task/{task_id}")
    def delete_item(self, task_id: int) -> APIMessage:
        task = get_task(task_id)
        session.delete(task)
        session.commit()
        return APIMessage(detail=f"Deleted task {task_id}")


APP.include_router(ROUTER)

if __name__ == "__main__":
    uvicorn.run(APP)
