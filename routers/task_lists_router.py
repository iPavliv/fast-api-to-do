from fastapi_utils.api_model import APIMessage
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import update, delete

from models import TaskList
from routers import session
from schemas.task_list_schemas import TListCreate, TListRead, TListUpdate
from utils import get_item_by_id

LIST_ROUTER = InferringRouter()


@cbv(LIST_ROUTER)
class TaskListView:
    @LIST_ROUTER.post("/task_list")
    async def create_item(self, task_list: TListCreate) -> TListRead:
        task_list_orm = TaskList(desc=task_list.desc, tasks=[])
        session.add(task_list_orm)
        await session.commit()
        return TListRead.from_orm(task_list_orm)

    @LIST_ROUTER.get("/task_list/{list_id}")
    async def read_item(self, list_id: int) -> TListRead:
        task_list_orm = await get_item_by_id(session, TaskList, list_id)
        return TListRead.from_orm(task_list_orm)

    @LIST_ROUTER.put("/task_list/{list_id}")
    async def update_item(self, list_id: int, task_list: TListUpdate) -> TListRead:
        task_list_orm = await get_item_by_id(session, TaskList, list_id)
        q = update(TaskList).where(TaskList.id == list_id)
        q = q.values(desc=task_list.desc)
        q.execution_options(synchronize_session="fetch")
        await session.execute(q)
        return TListRead.from_orm(task_list_orm)

    @LIST_ROUTER.delete("/task_list/{list_id}")
    async def delete_item(self, list_id: int) -> APIMessage:
        q = delete(TaskList).where(TaskList.id == list_id)
        await session.execute(q)
        return APIMessage(detail=f"Deleted task list {list_id}")
