from sqlalchemy.orm import Session

from comments import schemas
from comments.models import DBComment


def create_comment(db: Session, comment: schemas.CommentCreate):
    new_comment = DBComment(content=comment.content, post_id=comment.post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_comment(db: Session, comment_id: int):
    return db.query(DBComment).filter(DBComment.id == comment_id).first()


def get_comments(db: Session, post_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(DBComment)
        .filter(DBComment.post_id == post_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_comment(db: Session, comment_id: int, comment: schemas.CommentCreate):
    db_comment = db.query(DBComment).filter(DBComment.id == comment_id).first()
    if db_comment:
        db_comment.content = comment.content
        db.commit()
        db.refresh(db_comment)
        return db_comment
    return None


def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(DBComment).filter(DBComment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
        return db_comment
    return None
