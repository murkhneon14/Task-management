import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_and_get_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create task
        response = await ac.post("/tasks", json={"title": "Test Task"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["status"] == "pending"
        task_id = data["id"]

        # Get all tasks
        response = await ac.get("/tasks")
        assert response.status_code == 200
        tasks = response.json()
        assert any(t["id"] == task_id for t in tasks)

        # Update status
        response = await ac.patch(f"/tasks/{task_id}/status", json={"status": "completed"})
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

        # Delete task
        response = await ac.delete(f"/tasks/{task_id}")
        assert response.status_code == 204

        # Confirm deletion
        response = await ac.get("/tasks")
        assert all(t["id"] != task_id for t in response.json())
