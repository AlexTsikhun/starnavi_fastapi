from sqlalchemy.orm import Session

from posts.models import DBPost
from posts.schemas import PostCreate


def create_post(db: Session, post: PostCreate, user_id: int):
    new_post = DBPost(title=post.title, content=post.content, owner_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_post(db: Session, post_id: int):
    return db.query(DBPost).filter(DBPost.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBPost).offset(skip).limit(limit).all()


def update_post(db: Session, post_id: int, post: PostCreate):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post:
        db_post.title = post.title
        db_post.content = post.content
        db.commit()
        db.refresh(db_post)
        return db_post
    return None


def delete_post(db: Session, post_id: int):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return db_post
    return None
