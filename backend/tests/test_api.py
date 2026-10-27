import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
import models


# Separate in-memory database for testing
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_create_book(client):
    response = client.post(
        "/books/",
        json={
            "isbn": "9780132350884",
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "description": "A book about clean code.",
            "price": 32.50,
            "stock": 10,
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Clean Code"
    assert response.json()["stock"] == 10


def test_duplicate_isbn_is_rejected(client):
    book_data = {
        "isbn": "9780132350884",
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "description": "A book about clean code.",
        "price": 32.50,
        "stock": 10,
    }

    first_response = client.post("/books/", json=book_data)
    second_response = client.post("/books/", json=book_data)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_register_and_login(client):
    registration_response = client.post(
        "/users/register",
        json={
            "username": "testgebruiker",
            "email": "test@example.com",
            "password": "TestWachtwoord123!",
        },
    )

    assert registration_response.status_code == 201
    assert "password_hash" not in registration_response.json()

    login_response = client.post(
        "/users/login",
        data={
            "username": "testgebruiker",
            "password": "TestWachtwoord123!",
        },
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"

def test_reservation_reduces_stock(client):
    book_response = client.post(
        "/books/",
        json={
            "isbn": "9780132350884",
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "description": "A book about clean code.",
            "price": 32.50,
            "stock": 10,
        },
    )

    assert book_response.status_code == 201
    book_id = book_response.json()["id"]

    client.post(
        "/users/register",
        json={
            "username": "reserveerder",
            "email": "reserveerder@example.com",
            "password": "TestWachtwoord123!",
        },
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "reserveerder",
            "password": "TestWachtwoord123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    reservation_response = client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {token}"},
        json={"book_id": book_id, "quantity": 2},
    )

    assert reservation_response.status_code == 201

    updated_book_response = client.get(f"/books/{book_id}")

    assert updated_book_response.status_code == 200
    assert updated_book_response.json()["stock"] == 8


def test_reservation_rejects_insufficient_stock(client):
    book_response = client.post(
        "/books/",
        json={
            "isbn": "9780132350884",
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "description": "A book about clean code.",
            "price": 32.50,
            "stock": 2,
        },
    )

    assert book_response.status_code == 201
    book_id = book_response.json()["id"]

    client.post(
        "/users/register",
        json={
            "username": "reserveerder",
            "email": "reserveerder@example.com",
            "password": "TestWachtwoord123!",
        },
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "reserveerder",
            "password": "TestWachtwoord123!",
        },
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {token}"},
        json={"book_id": book_id, "quantity": 5},
    )

    assert response.status_code == 400

    updated_book_response = client.get(f"/books/{book_id}")

    assert updated_book_response.json()["stock"] == 2