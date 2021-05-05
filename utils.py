from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from models import Task


async def get_task(session: AsyncSession, task_id: int) -> Task:
    task = await session.execute(select(Task).where(Task.id == task_id))
    item_to_return = task.scalar()
    if not item_to_return:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return item_to_return
