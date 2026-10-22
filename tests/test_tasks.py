import pytest
from fastapi import status

def test_healthz(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_readyz(client):
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert "id" in data

def test_get_tasks(client):
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_update_task(client):
    response = client.post("/tasks", json={"title": "Initial Title"})
    task_id = response.json()["id"]
    
    update_response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Updated Title"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"

def test_delete_task(client):
    response = client.post("/tasks", json={"title": "Delete Me"})
    task_id = response.json()["id"]
    
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = client.get(f"/tasks/{task_id}") # This endpoint isn't implemented, but we check /tasks
    all_tasks = client.get("/tasks").json()
    assert not any(task["id"] == task_id for task in all_tasks)

def test_update_nonexistent_task(client):
    response = client.patch("/tasks/9999", json={"title": "Nope"})
    assert response.status_code == 404

def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/9999")
    assert response.status_code == 404
