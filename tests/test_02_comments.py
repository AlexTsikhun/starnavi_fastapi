import time
from datetime import datetime, timedelta


def get_id_of_created_post(
    client, auth_header, title="Test Post", content="This is a test post."
):
    response = client.post(
        "/api/v1/posts/",
        json={"title": title, "content": content},
        headers=auth_header,
    )
    return response.json()["id"]


def create_comment(client, auth_header, content, post_id):
    return client.post(
        "/api/v1/comments/",
        json={"content": content, "post_id": post_id},
        headers=auth_header,
    )


def get_comment_id(comment):
    return comment.json()["id"]


def update_comment(client, auth_header, comment_id, content, post_id):
    return client.put(
        f"/api/v1/comments/{comment_id}",
        json={"content": content, "post_id": post_id},
        headers=auth_header,
    )


def delete_comment(client, auth_header, comment_id):
    return client.delete(f"/api/v1/comments/{comment_id}", headers=auth_header)


def test_create_comment(client, auth_header):
    post_id = get_id_of_created_post(client, auth_header)

    response = create_comment(client, auth_header, "This is a comment.", post_id)
    assert response.status_code == 200
    assert response.json()["content"] == "This is a comment."


def test_create_comment_with_profanity(client, auth_header):
    post_id = get_id_of_created_post(client, auth_header)
    response = create_comment(client, auth_header, "This is a damn comment.", post_id)
    assert response.status_code == 400
    assert response.json() == {"detail": "The comment contains profanity"}


def test_get_comments(client, auth_header):
    time.sleep(15)
    post_id = get_id_of_created_post(client, auth_header)

    create_comment(client, auth_header, "Sweet)", post_id)
    create_comment(client, auth_header, "Хороша!", post_id)

    response = client.get(f"/api/v1/comments/?post_id={post_id}", headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_comment(client, auth_header):
    time.sleep(15)
    post_id = get_id_of_created_post(client, auth_header)

    comment = create_comment(client, auth_header, "This is a comment.", post_id)
    comment_id = get_comment_id(comment)

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
    post_id = get_id_of_created_post(client, auth_header)
    comment = create_comment(client, auth_header, "lol", post_id)
    comment_id = get_comment_id(comment)

    response = update_comment(client, auth_header, comment_id, "lol, funny", post_id)
    assert response.status_code == 200
    assert response.json()["content"] == "lol, funny"


def test_update_comment_with_profanity(client, auth_header):
    time.sleep(15)
    post_id = get_id_of_created_post(client, auth_header)
    comment = create_comment(client, auth_header, "Great pic", post_id)
    comment_id = get_comment_id(comment)

    response = update_comment(
        client, auth_header, comment_id, "This is a damn update.", post_id
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "The comment contains profanity"}


def test_delete_comment(client, auth_header):
    time.sleep(15)
    post_id = get_id_of_created_post(client, auth_header)
    comment = create_comment(client, auth_header, "This is a comment.", post_id)
    comment_id = get_comment_id(comment)

    response = delete_comment(client, auth_header, comment_id)
    assert response.status_code == 200
    assert response.json()["message"] == "Comment deleted successfully"


def test_delete_comment_not_found(client, auth_header):
    response = delete_comment(client, auth_header, 999)
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}


def test_comments_daily_breakdown(client, auth_header):
    time.sleep(15)
    post_id = get_id_of_created_post(client, auth_header)

    create_comment(client, auth_header, "Cool", post_id)
    create_comment(client, auth_header, "Not bad", post_id)

    today = datetime.utcnow()
    date_from = (today - timedelta(days=1)).strftime("%d-%m-%Y")
    date_to = today.strftime("%d-%m-%Y")

    response = client.get(
        f"/api/v1/comments-daily-breakdown?date_from={date_from}&date_to={date_to}",
        headers=auth_header,
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
