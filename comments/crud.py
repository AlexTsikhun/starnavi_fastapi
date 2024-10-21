from sqlalchemy.orm import Session

from comments import schemas
from comments.models import DBComment
from gemini import profanity_checker
from datetime import datetime


def create_comment(
    db: Session, comment: schemas.CommentCreate, user_id: int
) -> DBComment:
    is_blocked = profanity_checker(comment.content)
    new_comment = DBComment(
        content=comment.content,
        post_id=comment.post_id,
        user_id=user_id,
        created_at=datetime.utcnow(),
        is_blocked=is_blocked,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_comment(db: Session, comment_id: int):
    return (
        db.query(DBComment)
        .filter(DBComment.id == comment_id, DBComment.is_blocked == 0)
        .first()
    )


def get_comments(db: Session, post_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(DBComment)
        .filter(DBComment.post_id == post_id, DBComment.is_blocked == 0)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_comment(db: Session, comment_id: int, comment: schemas.CommentCreate):
    db_comment = (
        db.query(DBComment)
        .filter(DBComment.id == comment_id, DBComment.is_blocked == 0)
        .first()
    )
    if db_comment:
        is_blocked = profanity_checker(comment.content)

        db_comment.content = comment.content
        db_comment.is_blocked = is_blocked
        db.commit()
        db.refresh(db_comment)
        return db_comment
    return None


def delete_comment(db: Session, comment_id: int):
    db_comment = (
        db.query(DBComment)
        .filter(DBComment.id == comment_id, DBComment.is_blocked == 0)
        .first()
    )
    if db_comment:
        db.delete(db_comment)
        db.commit()
        return db_comment
    return None
