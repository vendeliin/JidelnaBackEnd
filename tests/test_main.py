from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

test_user = {"id": "1", "name": "John Doe", "grade": 1, "lunches": [{"lunch_out":1,"type_of_lunch":1,"id":1,"owner_id":"1"}]}

def test_post_user():
    response = client.post("/users", json=test_user)
    assert response.status_code == 200
    assert response.json() == "John Doe"


def test_update_user_lunch():
    response = client.put(f"/users/{test_user['name']}/lunches/1")
    assert response.status_code == 200
    assert response.json() == True


def test_get_users_count_rest():
    response = client.get("/users/total")
    assert response.status_code == 200
    assert response.json() == 1


def test_get_all_users_who_have_lunch():
    response = client.get("/users/lunch")
    assert response.status_code == 200
    assert response.json() == 0


def test_get_user_by_id():
    response = client.get(f"/users/{test_user['id']}")
    assert response.status_code == 200
    assert response.json() == test_user


def test_get_user_name():
    response = client.get(f"/users/{test_user['id']}/name")
    assert response.status_code == 200
    assert response.json() == test_user['name']


def test_get_users_with_lunch_out():
    response = client.get("/users/lunch/out")
    assert response.status_code == 200
    assert response.json() == 0


def test_get_count_of_lunches_rest():
    response = client.get("/lunches/rest/total")
    assert response.status_code == 200
    assert response.json() == 0

def test_post_admin():
    response = client.post("/admins", json={"name": "admin", "password": "password"})
    assert response.status_code == 200
    assert response.json() == "admin"


def test_post_login():
    client.post("/admins", json={"name": "admin", "password": "password"})
    response = client.post("/admins/login", json={"name": "admin", "password": "password"})
    assert response.status_code == 200
    assert response.json() == True


def test_delete_user():
    client.post("/users", json=test_user)
    response = client.delete(f"/users/{test_user['id']}")
    assert response.status_code == 200
    assert response.json() == test_user['name']


def test_delete_user_by_grade():
    client.post("/users", json=test_user)
    response = client.delete(f"/users/grade/{test_user['grade']}")
    assert response.status_code == 200
    assert response.json() == test_user['grade']












