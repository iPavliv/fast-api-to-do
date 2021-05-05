from fastapi_utils.api_model import APIMessage
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import update, delete

from models import Task
from routers import session
from schemas import TODOCreate, TODOUpdate, TODORead
from utils import get_task

ROUTER = InferringRouter()


@cbv(ROUTER)
class TaskView:
    @ROUTER.post("/task")
    async def create_item(self, task: TODOCreate) -> TODORead:
        task_orm = Task(desc=task.desc)
        session.add(task_orm)
        await session.commit()
        return TODORead.from_orm(task_orm)

    @ROUTER.get("/task/{task_id}")
    async def read_item(self, task_id: int) -> TODORead:
        task_orm = await get_task(session, task_id)
        return TODORead.from_orm(task_orm)

    @ROUTER.put("/task/{task_id}")
    async def update_item(self, task_id: int, task: TODOUpdate) -> TODORead:
        task_orm = await get_task(session, task_id)
        q = update(Task).where(Task.id == task_id)
        if task.desc:
            q = q.values(desc=task.desc)
        if task.completed:
            q = q.values(completed=task.completed)
        q.execution_options(synchronize_session="fetch")
        await session.execute(q)
        return TODORead.from_orm(task_orm)

    @ROUTER.delete("/task/{task_id}")
    async def delete_item(self, task_id: int) -> APIMessage:
        q = delete(Task).where(Task.id == task_id)
        await session.execute(q)
        return APIMessage(detail=f"Deleted task {task_id}")
