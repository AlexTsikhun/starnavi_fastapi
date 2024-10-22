def register_user(client, email="test@example.com", password="password123"):
    return client.post(
        "/api/v1/user/register/",
        json={"email": email, "password": password},
    )


def login_user(client, email="test@example.com", password="password123"):
    return client.post(
        "/api/v1/user/token",
        data={"username": email, "password": password},
    )


def get_user_me(client, access_token):
    return client.get(
        "/api/v1/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )


def update_auto_reply(client, access_token):
    return client.put(
        "/api/v1/user/auto-reply", headers={"Authorization": f"Bearer {access_token}"}
    )


def test_register(client):
    response = register_user(client)
    assert response.status_code == 200
    assert response.json() == {"username": "test@example.com"}

    response = register_user(client)
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_login(client):
    register_user(client)

    response = login_user(client)
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Invalid login
    response = login_user(client, password="wrongpassword")
    assert response.status_code == 400
    assert response.json() == {"detail": "Wrong email or password"}


def test_read_users_me(client):
    register_user(client)
    login_response = login_user(client)
    access_token = login_response.json()["access_token"]

    response = get_user_me(client, access_token)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_update_auto_reply(client):
    register_user(client)
    login_response = login_user(client)
    access_token = login_response.json()["access_token"]

    response = get_user_me(client, access_token)
    assert response.status_code == 200
    assert response.json()["auto_reply_enabled"] is False

    response = update_auto_reply(client, access_token)
    assert response.status_code == 200
    assert response.json()["previous_state"] is False
    assert response.json()["new_state"] is True

    # Toggle back
    response = update_auto_reply(client, access_token)
    assert response.status_code == 200
    assert response.json()["previous_state"] is True
    assert response.json()["new_state"] is False
