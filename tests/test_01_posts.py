def test_create_post(client, auth_header):
    response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"


def test_create_post_with_profanity(client, auth_header):
    response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a damn test post."},
        headers=auth_header,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "The post contains profanity"}


def test_get_posts(client, auth_header):
    client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    response = client.get("/api/v1/posts/", headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_post(client, auth_header):
    post_response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    post_id = post_response.json()["id"]

    response = client.get(f"/api/v1/posts/{post_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["id"] == post_id


def test_get_post_not_found(client, auth_header):
    response = client.get("/api/v1/posts/999", headers=auth_header)
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}


def test_update_post(client, auth_header):
    post_response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    post_id = post_response.json()["id"]

    response = client.put(
        f"/api/v1/posts/{post_id}",
        json={"title": "Updated Post", "content": "Updated content."},
        headers=auth_header,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Post"


def test_update_post_with_profanity(client, auth_header):
    post_response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    post_id = post_response.json()["id"]

    response = client.put(
        f"/api/v1/posts/{post_id}",
        json={"title": "Updated Post", "content": "This is a damn update."},
        headers=auth_header,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "The post contains profanity"}


def test_delete_post(client, auth_header):
    post_response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    post_id = post_response.json()["id"]

    response = client.delete(f"/api/v1/posts/{post_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["id"] == post_id


def test_delete_post_not_found(client, auth_header):
    response = client.delete("/api/v1/posts/999", headers=auth_header)
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}
