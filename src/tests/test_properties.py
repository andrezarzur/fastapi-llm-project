from src.api.routers.properties import router
from fastapi import FastAPI
from src.api.dependencies import validate_token_dependency, get_db
from src.domains.properties.models import Property
from src.config.database import Base
from src.config.setting import Settings
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.domains.properties.repositories import PropertyRepository


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


def test_get_properties(test_db):
    db = next(override_get_db())
    property_repo = PropertyRepository(db)

    property_repo.create(Property(
        property_type="HOUSE",
        address_full="0000 Avenida Brigadeiro Faria Lima, São Paulo - SP - Brasil",
        price="500000.00",
        area="150",
        parking="1",
        bedrooms="2",
        bathrooms="3",
        description="test",
        coordinates="0 0"
    ))

    response = client.get("/properties")
    assert response.status_code == 200

    properties = response.json()

    assert len(properties) == 1
    assert properties[0]['address_full'] == "0000 Avenida Brigadeiro Faria Lima, São Paulo - SP - Brasil"

def test_get_property(test_db):
    db = next(override_get_db())
    property_repo = PropertyRepository(db)

    new_property = property_repo.create(Property(
        property_type="HOUSE",
        address_full="0000 Avenida Brigadeiro Faria Lima, São Paulo - SP - Brasil",
        price="500000.00",
        area="150",
        parking="1",
        bedrooms="2",
        bathrooms="3",
        description="test",
        coordinates="0 0"
    ))

    response = client.get("/properties/" + str(new_property.id))
    assert response.status_code == 200

    property = response.json()
    assert property["address_full"] == "0000 Avenida Brigadeiro Faria Lima, São Paulo - SP - Brasil"


def test_create_property(test_db):
    new_property = {
      "property_type": "HOUSE",
      "address_full": "494 Rua Schilling, São Paulo - SP - Brasil",
      "price": 500000.00,
      "area": 150,
      "bedrooms": 3,
      "bathrooms": 2,
      "parking": 1
    }

    response = client.post("/properties/", json=new_property)
    assert response.status_code == 200
    property = response.json()
    assert property["address_full"] == "494 Rua Schilling, São Paulo - SP - Brasil"


def test_update_user(test_db):
    db = next(override_get_db())
    property_repo = PropertyRepository(db)

    new_property = property_repo.create(Property(
        property_type="HOUSE",
        address_full="0000 Avenida Brigadeiro Faria Lima, São Paulo - SP - Brasil",
        price="500000.00",
        area="150",
        parking="1",
        bedrooms="2",
        bathrooms="3",
        description="test",
        coordinates="0 0"
    ))

    update_property = {
      "property_type": "APARTMENT",
      "address_full": "0100 Avenida Brigadeiro Faria Lima, São Paulo - SP - Brasil",
      "price": 52220.00,
      "area": 15022,
      "bedrooms": 322,
      "bathrooms": 222,
      "parking": 122
    }

    response = client.put("/properties/" + str(new_property.id), json=update_property)
    assert response.status_code == 200
    user = response.json()
    assert user["address_full"] == "0100 Avenida Brigadeiro Faria Lima, São Paulo - SP - Brasil"


def test_delete_user(test_db):
    db = next(override_get_db())
    property_repo = PropertyRepository(db)

    new_property = property_repo.create(Property(
        property_type="HOUSE",
        address_full="0000 Avenida Brigadeiro Faria Lima, São Paulo - SP - Brasil",
        price="500000.00",
        area="150",
        parking="1",
        bedrooms="2",
        bathrooms="3",
        description="test",
        coordinates="0 0"
    ))

    response = client.delete("/properties/" + str(new_property.id))
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Property deleted successfully."
