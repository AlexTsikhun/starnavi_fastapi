def create_post(client, auth_header, title="Test Post", content="This is a test post."):
    response = client.post(
        "/api/v1/posts/",
        json={"title": title, "content": content},
        headers=auth_header,
    )
    return response


def get_post(client, auth_header, post_id):
    return client.get(f"/api/v1/posts/{post_id}", headers=auth_header)


def update_post(client, auth_header, post_id, title, content):
    return client.put(
        f"/api/v1/posts/{post_id}",
        json={"title": title, "content": content},
        headers=auth_header,
    )


def delete_post(client, auth_header, post_id):
    return client.delete(f"/api/v1/posts/{post_id}", headers=auth_header)


def test_create_post(client, auth_header):
    response = create_post(client, auth_header)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"


def test_create_post_with_profanity(client, auth_header):
    response = create_post(client, auth_header, content="This is a damn test post.")
    assert response.status_code == 400
    assert response.json() == {"detail": "The post contains profanity"}


def test_get_posts(client, auth_header):
    create_post(client, auth_header)
    response = client.get("/api/v1/posts/", headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_post(client, auth_header):
    post_response = create_post(client, auth_header)
    post_id = post_response.json()["id"]
    response = get_post(client, auth_header, post_id)
    assert response.status_code == 200
    assert response.json()["id"] == post_id


def test_get_post_not_found(client, auth_header):
    response = get_post(client, auth_header, 999)
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}


def test_update_post(client, auth_header):
    post_response = create_post(client, auth_header)
    post_id = post_response.json()["id"]
    response = update_post(
        client, auth_header, post_id, "Updated Post", "Updated content."
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Post"


def test_update_post_with_profanity(client, auth_header):
    post_response = create_post(client, auth_header)
    post_id = post_response.json()["id"]
    response = update_post(
        client, auth_header, post_id, "Updated Post", "This is a damn update."
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "The post contains profanity"}


def test_delete_post(client, auth_header):
    post_response = create_post(client, auth_header)
    post_id = post_response.json()["id"]
    response = delete_post(client, auth_header, post_id)
    assert response.status_code == 200
    assert response.json()["id"] == post_id


def test_delete_post_not_found(client, auth_header):
    response = delete_post(client, auth_header, 999)
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}
