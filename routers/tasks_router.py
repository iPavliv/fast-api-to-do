from fastapi_utils.api_model import APIMessage
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import update, delete

from models import Task
from routers import session
from schemas.task_schemas import TODOCreate, TODOUpdate, TODORead
from utils import get_item_by_id

TASK_ROUTER = InferringRouter()


@cbv(TASK_ROUTER)
class TaskView:
    @TASK_ROUTER.post("/task_list/{list_id}/task")
    async def create_item(self, task: TODOCreate) -> TODORead:
        task_orm = Task(desc=task.desc, list_id=task.list_id)
        session.add(task_orm)
        await session.commit()
        return TODORead.from_orm(task_orm)

    @TASK_ROUTER.get("/task_list/{list_id}/task/{task_id}")
    async def read_item(self, task_id: int) -> TODORead:
        task_orm = await get_item_by_id(session, Task, task_id)
        return TODORead.from_orm(task_orm)

    @TASK_ROUTER.put("/task_list/{list_id}/task/{task_id}")
    async def update_item(self, task_id: int, task: TODOUpdate) -> TODORead:
        task_orm = await get_item_by_id(session, Task, task_id)
        q = update(Task).where(Task.id == task_id)
        if task.desc:
            q = q.values(desc=task.desc)
        if task.completed:
            q = q.values(completed=task.completed)
        q.execution_options(synchronize_session="fetch")
        await session.execute(q)
        return TODORead.from_orm(task_orm)

    @TASK_ROUTER.delete("/task_list/{list_id}/task/{task_id}")
    async def delete_item(self, task_id: int) -> APIMessage:
        q = delete(Task).where(Task.id == task_id)
        await session.execute(q)
        return APIMessage(detail=f"Deleted task {task_id}")
