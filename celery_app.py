from celery import Celery

from comments.models import DBComment
from dependencies import get_db
from gemini import gemini_auto_reply
from posts.models import DBPost

celery = Celery("tasks", broker="redis://localhost:6379/0")


@celery.task
def auto_reply(comment_id, post_id, user_id):
    db = next(get_db())  # or SessionLocal()

    comment = db.query(DBComment).filter(DBComment.id == comment_id).first()
    post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if comment and post:
        reply_content = gemini_auto_reply(post.content, comment.content)
        new_reply = DBComment(content=reply_content, post_id=post_id, user_id=user_id)
        db.add(new_reply)
        db.commit()