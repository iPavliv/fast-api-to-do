from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND


async def get_item_by_id(session: AsyncSession, entity_name, entity_id: int):
    query_item = await session.execute(select(entity_name).where(entity_name.id == entity_id))

    item_to_return = query_item.scalar()
    if not item_to_return:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    return item_to_return
