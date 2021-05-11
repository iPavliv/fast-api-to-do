import pytest
from httpx import AsyncClient


@pytest.fixture(scope="module")
async def create_list_for_delete_test(app):
    async with AsyncClient(app=app, base_url=f"http://test/task_list") as ac:
        response = await ac.post("/", json={"desc": "Task list for delete test"})
    return response.json()["id"]


class TestListCreate:
    @pytest.mark.asyncio
    async def test_create_list_success(self, app):
        async with AsyncClient(app=app, base_url=f"http://test/task_list") as ac:
            response = await ac.post("/", json={"desc": "Test task list"})
        assert response.status_code == 200
        assert "id" in response.json()


class TestListRead:
    @pytest.mark.asyncio
    async def test_read_list_success(self, create_list, app):
        list_id = create_list["id"]
        expected_list = dict(create_list)
        async with AsyncClient(app=app, base_url=f"http://test/task_list/{list_id}") as ac:
            response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == expected_list


class TestListUpdate:
    @pytest.mark.asyncio
    async def test_update_list_success(self, create_list, app):
        list_id = create_list["id"]
        list_to_update = {"desc": "Brand new description"}
        async with AsyncClient(app=app, base_url=f"http://test/task_list/{list_id}") as ac:
            response = await ac.put("/", json=list_to_update)
        assert response.status_code == 200
        assert response.json()["desc"] == list_to_update["desc"]


class TestListDelete:
    @pytest.mark.asyncio
    async def test_delete_list_success(self, create_list_for_delete_test, app):
        list_id = create_list_for_delete_test
        async with AsyncClient(app=app, base_url=f"http://test/task_list/{list_id}") as ac:
            response = await ac.delete("/")
        assert response.status_code == 200
        assert response.text == f'{{"detail":"Deleted task list {list_id}"}}'
