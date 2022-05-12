from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_task_1():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"start": "1970-01-01"}

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
    response = client.put("/events", json={"date": "2022-03-01", "event": "Dzień Balearów"})

    response_data = response.json()

    del response_data["id"]
    del response_data["date_added"]

    assert response.status_code == 200
    assert response_data == {
        "name": "Dzień Balearów",
        "date": "2022-03-01"
    }

def test_task_5():
    response = client.put("/events", json={"date": "2022-03-22", "event": "Drugi dzień wiosny"})

    assert response.status_code == 200

    retrieve_response = client.get("/event/2022-03-22")

    assert retrieve_response.status_code == 200

    assert retrieve_response.json()[0]["name"] == "Drugi dzień wiosny"