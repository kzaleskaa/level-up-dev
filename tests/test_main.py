from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_task_1():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"start": "1970-01-0"}

def test_task_2_get():
    response = client.get("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}

def test_task_2_options():
    response = client.options("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "OPTIONS"}

def test_task_2_delete():
    response = client.delete("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}

def test_task_2_post():
    response = client.post("/method")
    assert response.status_code == 201
    assert response.json() == {"method": "POST"}
    
def test_task_3_correct():
    response = client.get("/day?name=monday&number=1")
    assert  response.status_code == 200

def test_task_3_incorrect():
    response = client.get("/day?name=tuesday&number=3")
    assert response.status_code == 400

def test_task_4():
    response = client.put("/events", json={"date": "2021-01-01", "name": "Event name"})

    response_data = response.json()

    del response_data["id"]
    del response_data["date_added"]

    assert response.status_code == 200
    assert response_data == {
        "name": "Event name",
        "date": "2021-01-01"
    }
