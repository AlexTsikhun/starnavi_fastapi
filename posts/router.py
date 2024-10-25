from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from core.database import get_db
from gemini import profanity_checker
from posts import schemas
from posts.crud import create_post, get_posts, get_post, update_post, delete_post
from user.models import DBUser
from user.oauth2 import get_current_user

router = APIRouter()


@router.post("/posts/", response_model=schemas.Post)
def create_post_endpoint(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    if profanity_checker(post.content):
        raise HTTPException(status_code=400, detail="The post contains profanity")
    return create_post(db, post, current_user.id)


@router.get("/posts/", response_model=list[schemas.Post])
def get_posts_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_posts(db, skip=skip, limit=limit)


@router.get("/posts/{post_id}", response_model=schemas.Post)
def get_post_endpoint(post_id: int, db: Session = Depends(get_db)):
    db_post = get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put(
    "/posts/{post_id}",
    response_model=schemas.Post,
    dependencies=[Depends(get_current_user)],
)
def update_post_endpoint(
    post_id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
):
    db_post = update_post(db, post_id, post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if profanity_checker(post.content):
        raise HTTPException(status_code=400, detail="The post contains profanity")
    return db_post


@router.delete(
    "/posts/{post_id}",
    response_model=schemas.DeletePostResponse,
    dependencies=[Depends(get_current_user)],
)
def delete_post_endpoint(post_id: int, db: Session = Depends(get_db)):
    db_post = delete_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully", "deleted_post": db_post}
