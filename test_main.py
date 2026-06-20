from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post("/tasks", json={"title": "Write tests"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["done"] is False


def test_get_tasks_grows():
    response_before = client.get("/tasks")
    count_before = len(response_before.json())

    client.post("/tasks", json={"title": "Another task"})

    response_after = client.get("/tasks")
    tasks_after = response_after.json()
    assert isinstance(tasks_after, list)
    assert len(tasks_after) == count_before + 1


def test_create_task_empty_title_fails():
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400
