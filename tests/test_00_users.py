import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from user.models import Base, DBUser
from main import app  # Replace with the correct import for your FastAPI app
from dependencies import get_db


def test_register(client):
    response = client.post(
        "/api/v1/user/register/",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert response.json() == {"username": "test@example.com"}

    response = client.post(
        "/api/v1/user/register/",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_login(client):
    client.post(
        "/api/v1/user/register/",
        json={"email": "test@example.com", "password": "password123"},
    )

    response = client.post(
        "/api/v1/user/token",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Invalid login
    response = client.post(
        "/api/v1/user/token",
        data={"username": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Wrong email or password"}


def test_read_users_me(client):
    client.post(
        "/api/v1/user/register/",
        json={"email": "test@example.com", "password": "password123"},
    )
    login_response = client.post(
        "/api/v1/user/token",
        data={"username": "test@example.com", "password": "password123"},
    )
    access_token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_update_auto_reply(client):
    client.post(
        "/api/v1/user/register/",
        json={"email": "test@example.com", "password": "password123"},
    )
    login_response = client.post(
        "/api/v1/user/token",
        data={"username": "test@example.com", "password": "password123"},
    )
    access_token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["auto_reply_enabled"] is False

    response = client.put(
        "/api/v1/user/auto-reply", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["previous_state"] is False
    assert response.json()["new_state"] is True

    # Toggle back
    response = client.put(
        "/api/v1/user/auto-reply", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["previous_state"] is True
    assert response.json()["new_state"] is False
