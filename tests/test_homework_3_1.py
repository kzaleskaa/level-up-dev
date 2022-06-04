from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from main import app

client = TestClient(app)


def test_task_3_1():
    response = client.get("/start")
    html_content = "<h1>The unix epoch started at 1970-01-01</h1>"
    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]
    assert html_content in response.content.decode()


def test_task_correct_3_2():
    response = client.post("/check", auth=HTTPBasicAuth(username="username", password="1999-02-02"))
    assert response.status_code == 200


def test_task_incorrrect_3_2():
    response = client.post("/check", auth=HTTPBasicAuth(username="username", password="2022-03-03"))
    assert response.status_code == 401


def test_task_json_3_3():
    response = client.get("/info", params={"format": "json"}, headers={"User-Agent": "x"})
    assert response.json() == {"user_agent": "x"}


def test_task_html_3_3():
    response = client.get("/info", params={"format": "html"}, headers={"User-Agent": "x"})
    html_content = f'<input type="text" id=user-agent name=agent value="x">'
    assert html_content in response.content.decode()


def test_task_3_3_incorrect_format():
    response = client.get("/info", params={"format": "abc"}, headers={"User-Agent": "x"})
    assert response.status_code == 400


def test_task_3_3_no_format():
    response = client.get("/info", headers={"User-Agent": "x"})
    assert response.status_code == 400


def test_task_3_4_no_path():
    response = client.get("save/abc")
    assert response.status_code == 404


def test_task_3_5_put_path():
    response = client.put("save/new-path123")
    assert response.status_code == 200


def test_task_3_5_redirect():
    response_put = client.put("save/123path")
    assert response_put.status_code == 200

    response_get = client.get("save/123path", allow_redirects=False)
    assert response_get.status_code == 301
    assert "info" in response_get.headers["Location"]


def test_task_3_5_delete_path():
    response_put = client.put("save/add_path")
    assert response_put.status_code == 200

    response_get = client.get("save/add_path", allow_redirects=False)
    assert response_get.status_code == 301
    assert "info" in response_get.headers["Location"]

    response_delete = client.delete("save/add_path")
    assert response_delete.status_code == 200

    response_get = client.get("save/add_path", allow_redirects=False)
    assert response_get.status_code == 404


def test_task_3_5_patch():
    response_patch = client.patch("save/add_path")
    assert response_patch.status_code == 400
