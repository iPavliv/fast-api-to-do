import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import delete

from models import Base, TaskList
from routers.task_lists_router import LIST_ROUTER
from routers.tasks_router import TASK_ROUTER
from utils import get_session


@pytest.yield_fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app():
    app = FastAPI()

    app.include_router(TASK_ROUTER)
    app.include_router(LIST_ROUTER)
    yield app


# @pytest.fixture(scope="session")
# async def session(app):
#     session = get_session()
#     # Base.metadata.drop_all()
#     # Base.metadata.create_all()
#     yield session
#     # session.delete(TaskList)
#     await session.execute(delete(TaskList))


@pytest.fixture(scope="session")
async def create_list(app):
    async with AsyncClient(app=app, base_url="http://test/task_list") as ac:
        response = await ac.post("/", json={"desc": "task list for task tests"})
    return response.json()
