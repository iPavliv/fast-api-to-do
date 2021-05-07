from fastapi import Depends, HTTPException
from fastapi_utils.api_model import APIMessage
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import update, delete, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST

from models import Task
from schemas.task_schemas import TODOCreate, TODOUpdate, TODORead
from utils import get_session, get_task_by_id

TASK_ROUTER = InferringRouter()


@cbv(TASK_ROUTER)
class TaskView:
    @TASK_ROUTER.post("/task_list/{list_id}/task")
    async def create_item(
            self, list_id: int, task: TODOCreate, session: AsyncSession = Depends(get_session)
    ) -> TODORead:
        task_orm = Task(desc=task.desc, list_id=list_id)
        session.add(task_orm)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid list id")
        return TODORead.from_orm(task_orm)

    @TASK_ROUTER.get("/task_list/{list_id}/task/{task_id}")
    async def read_item(
            self, list_id: int, task_id: int, session: AsyncSession = Depends(get_session)
    ) -> TODORead:
        task_orm = await get_task_by_id(session, list_id, task_id)
        return TODORead.from_orm(task_orm)

    @TASK_ROUTER.put("/task_list/{list_id}/task/{task_id}")
    async def update_item(
            self, list_id: int, task_id: int, task: TODOUpdate, session: AsyncSession = Depends(get_session)
    ) -> TODORead:
        task_orm = await get_task_by_id(session, list_id, task_id)
        q = update(Task).where(and_(Task.id == task_id, Task.list_id == list_id))
        # for k, v in vars(task).items():
        #     q = q.values(k=v)
        if task.desc:
            q = q.values(desc=task.desc)
        if task.completed in (True, False):
            q = q.values(completed=task.completed)
        q.execution_options(synchronize_session="fetch")
        await session.execute(q)
        return TODORead.from_orm(task_orm)

    @TASK_ROUTER.delete("/task_list/{list_id}/task/{task_id}")
    async def delete_item(self, list_id: int, task_id: int, session: AsyncSession = Depends(get_session)) -> APIMessage:
        q = delete(Task).where(and_(Task.id == task_id, Task.list_id == list_id))
        await session.execute(q)
        return APIMessage(detail=f"Deleted task {task_id} from list {list_id}")
