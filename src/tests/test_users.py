from src.api.routers.users import router
from fastapi import FastAPI
from src.api.dependencies import validate_token_dependency, get_db
from src.domains.users.models import User
from src.config.database import Base
from src.config.setting import Settings
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.domains.users.repositories import UserRepository


SQLALCHEMY_DATABASE_URL = Settings().TESTING_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_oauth2_scheme():
    return "mocked-test-token"


app = FastAPI()
app.include_router(router)


app.dependency_overrides[validate_token_dependency] = override_get_oauth2_scheme
app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_get_users(test_db):
    db = next(override_get_db())
    user_repo = UserRepository(db)

    user1 = user_repo.create(User(
        email="test1@example.com",
        fantasy_name="Test User 1",
        password="hashed_password_1",
        cnpj="98765432109"
    ))

    user2 = user_repo.create(User(
        email="test2@example.com",
        fantasy_name="Test User 2",
        password="hashed_password_2",
        cnpj="98765432109"
    ))

    response = client.get("/users/")
    assert response.status_code == 200

    users = response.json()
    assert len(users) == 2
    assert any(user["email"] == user1.email for user in users)
    assert any(user["email"] == user2.email for user in users)


def test_get_user(test_db):
    db = next(override_get_db())
    user_repo = UserRepository(db)

    new_user = user_repo.create(User(
        email="testget@example.com",
        fantasy_name="Test User 1",
        password="hashed_password_1",
        cnpj="98765432109"
    ))

    response = client.get("/users/" + str(new_user.id))
    assert response.status_code == 200

    user = response.json()
    assert user["email"] == "testget@example.com"


def test_create_user(test_db):
    new_user = {
        "email": "testcreate@example.com",
        "fantasy_name": "Test User 1",
        "password": "hashed_password_1",
        "cnpj": "98765432109"
    }

    response = client.post("/users/", json=new_user)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "testcreate@example.com"


def test_update_user(test_db):
    db = next(override_get_db())
    user_repo = UserRepository(db)
    new_user = user_repo.create(User(
        email="testupdatedcreated@example.com",
        fantasy_name="Test User",
        password="hashed_password",
        cnpj="98765432109"
    ))

    update_user = {
        "email": "testupdated@example.com",
        "fantasy_name": "Test User",
        "password": "hashed_password",
        "cnpj": "98765432109"
    }

    response = client.put("/users/" + str(new_user.id), json=update_user)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "testupdated@example.com"


def test_delete_user(test_db):
    db = next(override_get_db())
    user_repo = UserRepository(db)
    new_user = user_repo.create(User(
        email="testupdatedcreated@example.com",
        fantasy_name="Test User",
        password="hashed_password",
        cnpj="98765432109"
    ))

    response = client.delete("/users/" + str(new_user.id))
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "User deleted successfully."
