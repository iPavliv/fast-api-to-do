import pytest
from httpx import AsyncClient

task_dummy = {
    "desc": "task dummy description",
}

pre_added_task = {
    "desc": "to Do: write all tests",
}


@pytest.fixture(scope="module")
async def create_task(create_list, app):
    list_id = create_list["id"]
    async with AsyncClient(app=app, base_url=f"http://test/task_list/{list_id}") as ac:
        response = await ac.post("/task", json=pre_added_task)
    return response.json()


class TestTaskCreate:
    @pytest.mark.asyncio
    async def test_create_task_success(self, create_list, app):
        list_id = create_list["id"]
        async with AsyncClient(app=app, base_url=f"http://test/task_list/{list_id}") as ac:
            response = await ac.post("/task", json=task_dummy)
        assert response.status_code == 200
        assert "id" in response.json()

    @pytest.mark.asyncio
    async def test_create_task_fail_validation(self, create_list, app):
        list_id = create_list["id"]
        async with AsyncClient(app=app, base_url=f"http://test/task_list/{list_id}") as ac:
            response = await ac.post("/task", json={})
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_task_fail_creation(self, create_list, app):
        list_id = create_list["id"]
        async with AsyncClient(app=app, base_url=f"http://test/task_list/{list_id+1}") as ac:
            response = await ac.post("/task", json=task_dummy)
        assert response.status_code == 400
        assert response.text == '{"detail":"Invalid list id"}'


class TestTaskRead:
    @pytest.mark.asyncio
    async def test_read_task_success(self, create_list, create_task, app):
        list_id = create_list["id"]
        task_id = create_task["id"]
        expected_task = {"id": task_id, "list_id": list_id, "completed": False, **pre_added_task}
        async with AsyncClient(app=app, base_url=f"http://test/task_list/{list_id}/task/{task_id}") as ac:
            response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == expected_task

    @pytest.mark.asyncio
    async def test_read_task_fail(self, create_list, create_task, app):
        list_id = create_list["id"]
        task_id = create_task["id"]
        async with AsyncClient(app=app, base_url=f"http://test/task_list/{list_id}/task/{task_id+1}") as ac:
            response = await ac.get("/")
        assert response.status_code == 404


class TestTaskUpdate:
    @pytest.mark.asyncio
    async def test_update_task_success(self, create_list, create_task, app):
        list_id = create_list["id"]
        task_id = create_task["id"]
        task_to_update = {"completed": True, "desk": "Task Updated!"}
        async with AsyncClient(app=app, base_url=f"http://test/task_list/{list_id}/task/{task_id}") as ac:
            response = await ac.put("/", json=task_to_update)
        assert response.status_code == 200
        assert response.json()["completed"]


class TestTaskDelete:
    @pytest.mark.asyncio
    async def test_delete_task_success(self, create_list, create_task, app):
        list_id = create_list["id"]
        task_id = create_task["id"]
        async with AsyncClient(app=app, base_url=f"http://test/task_list/{list_id}/task/{task_id}") as ac:
            response = await ac.delete("/")
        assert response.status_code == 200
        assert response.text == f'{{"detail":"Deleted task {task_id} from list {list_id}"}}'
