from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException

from fastapi_utils.api_model import APIMessage
from fastapi_utils.cbv import cbv

from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import select, MetaData, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.status import HTTP_404_NOT_FOUND

from models import Task, Base
from schemas import TODOCreate, TODOUpdate


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://todos:todos@127.0.0.1:5432/todos"
metadata = MetaData()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# metadata.create_all(engine)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
session = SessionLocal()

APP = FastAPI()
ROUTER = InferringRouter()


# @APP.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.execute()
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)


async def get_task(task_id: int) -> Task:
    task: Optional[Task] = await session.execute(select(Task).where(Task.id == task_id))
    if not task:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return task


@cbv(ROUTER)
class TaskView:
    @ROUTER.post("/task/add")
    async def create_item(self, task: TODOCreate) -> TODOUpdate:
        task_orm = Task(desc=task.desc)
        session.add(task_orm)
        await session.commit()
        return TODOUpdate.from_orm(task_orm)

    @ROUTER.get("/task/{task_id}")
    async def read_item(self, task_id: int) -> TODOUpdate:
        task_orm = await get_task(task_id)
        # return TODOUpdate.from_orm(task_orm)
        return task_orm.scalar()

    @ROUTER.put("/task/{task_id}")
    async def update_item(self, task_id: int, task: TODOCreate) -> TODOUpdate:
        task_orm = await get_task(task_id)
        q = update(Task).where(Task.id == task_id)
        if task.desc:
            q = q.values(desc=task.desc)
        if task.completed:
            q = q.values(completed=task.completed)
        q.execution_options(synchronize_session="fetch")
        await session.execute(q)
        return task_orm.scalar()

    @ROUTER.delete("/task/{task_id}")
    async def delete_item(self, task_id: int) -> APIMessage:
        q = delete(Task).where(Task.id == task_id)
        await session.execute(q)
        return APIMessage(detail=f"Deleted task {task_id}")


APP.include_router(ROUTER)

if __name__ == "__main__":
    uvicorn.run(APP)
