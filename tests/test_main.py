from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.database import Base
from app.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

# disabling connection pooling with `poolclass=StaticPool`
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post("/create/user", json={"id": "1", "name": "Vendelin", "grade": 1, "lunches": []})
    assert response.status_code == 200
    assert response.json() == "Vendelin"


def test_create_admin():
    response = client.post("/create/admin", json={"name": "admin", "password": "1"})
    assert response.status_code == 200
    assert response.json() == "admin"


def test_login():
    response = client.post("/login", json={"name": "admin", "password": "1"})
    assert response.status_code == 200
    assert response.json() == True


def test_update_lunch():
    response = client.put("/user/Vendelin/update-lunch/1")
    assert response.status_code == 200
    assert response.json() == True


def test_get_user():
    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json() == {"grade": 1, "name": "Vendelin", "id": "1", 'lunches': [{
        'id': 1, 'lunch_out': 1, 'owner_id': '1', 'type_of_lunch': 1
    }]}


def test_users_with_lunch_out():
    response = client.get("/users/WithLunchOut")
    assert response.status_code == 200
    assert response.json() == 0


def test_get_all_users_who_have_lunch():
    response = client.get("/users/All")
    assert response.status_code == 200
    assert response.json() == [{"grade": 1, "name": "Vendelin", "id": "1", 'lunches': [{
        'id': 1, 'lunch_out': 1, 'owner_id': '1', 'type_of_lunch': 1
    }]}]


def test_get_lunches_count_rest():
    response = client.get("/lunches/count/rest")
    assert response.status_code == 200
    assert isinstance(response.json(), int)


def test_user_name():
    response = client.get("/user/name/1")
    assert response.status_code == 200
    assert response.json() == "Vendelin"


def test_get_lunches_count_out():
    response = client.get("/lunches/count/out")
    assert response.status_code == 200
    assert isinstance(response.json(), int)


def test_delete_user():
    response = client.delete("/user/delete/1")
    assert response.status_code == 200
    assert response.json() == "Vendelin"
