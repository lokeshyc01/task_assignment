from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest
from .main import app
from . import schema,model
from .database import SessionLocal
client = TestClient(app)

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_taks():
    task_data = {
        "title":"test title",
        "description":"test description",
        "duedate":"2024-04-12T12:00:00",
        "priority":"High"
    }
    print("test conducted")  
    response = client.post("/tasks",json=task_data)
    assert response.status_code == 401
    # task = response.json()
    # assert task["title"] == task_data["title"]
    # assert task["description"] == task_data["description"]
    # assert task["duedate"] == task_data["duedate"]
    # assert task["priority"] == task_data["priority"]

# def test_get_tasks(db:Session):
#     response_without_param = client.get("/tasks")
#     assert response_without_param.status_code == 200
#     assert isinstance(response_without_param.json(),list)

#     response_with_iscompleted = client.get("/tasks?is_completed=true")
#     assert response_with_iscompleted.status_code == 200
#     assert isinstance(response_with_iscompleted.json(),list)

#     response_with_priority = client.get("/task?priority=High")
#     assert response_with_priority.status_code == 200
#     assert isinstance(response_with_priority.json(),list)


def test_get_task():
    response = client.get("/tasks",params={"task_id":1})
    assert response.status_code == 401
    # assert isinstance(response.json(),schema.Task)


def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 401
    # assert response.text == "task deleted"


def test_update_task():
    task_data = {
        "title":"test title",
        "description":"test description",
        "priority":"High"
    }
    response = client.put("/tasks",json=task_data)
    assert response.status_code == 401
    task = response.json()
    # assert task["title"] == task_data["title"]
    # assert task["description"] == task_data["description"]
    # assert task["priority"] == task_data["priority"]

def test_create_user():
    response = client.post("/users/",json={"name":"random","password":"Lokesh@11"})
    assert response.status_code == 201
    # assert isinstance(response.json(),model.User)

def test_create_task_for_user():
    response = client.post("/users/{user_id}/items",json={"title":"new","description":"new desc","duedate":"2024-04-12T07:17:06.518Z","priority":"High"})
    assert response.status_code == 401
    # assert isinstance(response.json(),schema.Task)

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 401
    # assert isinstance(response.json(),list)

