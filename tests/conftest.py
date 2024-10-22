from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dependencies import get_db
from main import app  # Replace with the correct import for your FastAPI app
from user.models import Base, DBUser

import pytest

from fastapi.testclient import TestClient


# Create a new database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def create_test_user(client):
    response = client.post(
        "/api/v1/user/register/",
        json={"email": "test@example.com", "password": "password123"},
    )
    return response.json()


@pytest.fixture
def auth_header(create_test_user):
    client = TestClient(app)
    login_response = client.post(
        "/api/v1/user/token",
        data={"username": "test@example.com", "password": "password123"},
    )
    access_token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def mock_profanity_checker():
    with patch("gemini.profanity_checker") as mock:
        yield mock
