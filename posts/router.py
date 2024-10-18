from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from dependencies import get_db
from posts import schemas
from posts.crud import create_post, get_posts, get_post, update_post, delete_post

router = APIRouter()


@router.post("/posts/", response_model=schemas.Post)
def create_post_endpoint(
    post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = 1
):
    return create_post(db, post, user_id)


@router.get("/posts/", response_model=list[schemas.Post])
def get_posts_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_posts(db, skip=skip, limit=limit)


@router.get("/posts/{post_id}", response_model=schemas.Post)
def get_post_endpoint(post_id: int, db: Session = Depends(get_db)):
    db_post = get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/posts/{post_id}", response_model=schemas.Post)
def update_post_endpoint(
    post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    db_post = update_post(db, post_id, post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.delete("/posts/{post_id}", response_model=schemas.Post)
def delete_post_endpoint(post_id: int, db: Session = Depends(get_db)):
    db_post = delete_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
