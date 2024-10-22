import time


def test_create_comment(client, auth_header):
    post_response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    post_id = post_response.json()["id"]

    response = client.post(
        "/api/v1/comments/",
        json={"content": "This is a comment.", "post_id": post_id},
        headers=auth_header,
    )
    assert response.status_code == 200
    assert response.json()["content"] == "This is a comment."


def test_create_comment_with_profanity(client, auth_header):
    post_response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    post_id = post_response.json()["id"]

    response = client.post(
        "/api/v1/comments/",
        json={"content": "This is a damn comment.", "post_id": post_id},
        headers=auth_header,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "The comment contains profanity"}


def test_get_comments(client, auth_header):
    time.sleep(15)
    post_response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    post_id = post_response.json()["id"]

    client.post(
        "/api/v1/comments/",
        json={"content": "Sweet)", "post_id": post_id},
        headers=auth_header,
    )
    client.post(
        "/api/v1/comments/",
        json={"content": "Хороша!", "post_id": post_id},
        headers=auth_header,
    )

    response = client.get(f"/api/v1/comments/?post_id={post_id}", headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_comment(client, auth_header):
    time.sleep(15)

    post_response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    post_id = post_response.json()["id"]

    comment_response = client.post(
        "/api/v1/comments/",
        json={"content": "This is a comment.", "post_id": post_id},
        headers=auth_header,
    )
    comment_id = comment_response.json()["id"]

    response = client.get(f"/api/v1/comments/{comment_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["id"] == comment_id


def test_get_comment_not_found(client, auth_header):
    response = client.get("/api/v1/comments/999", headers=auth_header)
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}


def test_update_comment(client, auth_header):
    # to prevent 429 Resource has been exhausted (e.g. check quota) - pause in use API
    time.sleep(15)

    post_response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    post_id = post_response.json()["id"]

    comment_response = client.post(
        "/api/v1/comments/",
        json={"content": "lol", "post_id": post_id},
        headers=auth_header,
    )
    comment_id = comment_response.json()["id"]

    response = client.put(
        f"/api/v1/comments/{comment_id}",
        json={"content": "lol, funny", "post_id": post_id},
        headers=auth_header,
    )
    assert response.status_code == 200
    assert response.json()["content"] == "lol, funny"


def test_update_comment_with_profanity(client, auth_header):
    time.sleep(10)

    post_response = client.post(
        "/api/v1/posts/",
        json={"title": "Post", "content": "About life"},
        headers=auth_header,
    )
    post_id = post_response.json()["id"]

    comment_response = client.post(
        "/api/v1/comments/",
        json={"content": "Great pic", "post_id": post_id},
        headers=auth_header,
    )
    comment_id = comment_response.json()["id"]
    response = client.put(
        f"/api/v1/comments/{comment_id}",
        json={
            "content": "This is a damn update.",
            "post_id": post_id,
        },
        headers=auth_header,
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "The comment contains profanity"}


def test_delete_comment(client, auth_header):
    time.sleep(15)

    post_response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    post_id = post_response.json()["id"]

    comment_response = client.post(
        "/api/v1/comments/",
        json={"content": "This is a comment.", "post_id": post_id},
        headers=auth_header,
    )
    comment_id = comment_response.json()["id"]

    response = client.delete(f"/api/v1/comments/{comment_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["id"] == comment_id


def test_delete_comment_not_found(client, auth_header):
    response = client.delete("/api/v1/comments/999", headers=auth_header)
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}


def test_comments_daily_breakdown(client, auth_header):
    time.sleep(15)

    post_response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=auth_header,
    )
    post_id = post_response.json()["id"]

    client.post(
        "/api/v1/comments/",
        json={"content": "Cool", "post_id": post_id},
        headers=auth_header,
    )
    client.post(
        "/api/v1/comments/",
        json={"content": "Not bad", "post_id": post_id},
        headers=auth_header,
    )

    from datetime import datetime, timedelta

    today = datetime.utcnow()
    date_from = (today - timedelta(days=1)).strftime("%d-%m-%Y")
    date_to = today.strftime("%d-%m-%Y")

    response = client.get(
        f"/api/v1/comments-daily-breakdown?date_from={date_from}&date_to={date_to}",
        headers=auth_header,
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
