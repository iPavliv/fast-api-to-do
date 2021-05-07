import os

from fastapi import HTTPException
from sqlalchemy import select, and_
from starlette.status import HTTP_404_NOT_FOUND

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import settings
from models import Task
from schemas.task_schemas import TODORead

config = settings.get(os.environ.get("ENV_NAME"))()
SQLALCHEMY_DATABASE_URL = config.database_url
metadata = MetaData()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, execution_options={
        "isolation_level": config.isolation_level
    })

ASYNC_SESSION = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with ASYNC_SESSION() as session:
        yield session


async def get_task_by_id(session: AsyncSession, list_id: int, task_id: int) -> TODORead:
    query_item = await session.execute(select(Task).where(and_(Task.id == task_id, Task.list_id == list_id)))

    item_to_return = query_item.scalar()
    if not item_to_return:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    return item_to_return


async def get_item_by_id(session: AsyncSession, entity_name, entity_id: int):
    query_item = await session.execute(select(entity_name).where(entity_name.id == entity_id))

    item_to_return = query_item.scalar()
    if not item_to_return:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    return item_to_return
