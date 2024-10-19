from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from comments import schemas
from comments.crud import (
    create_comment,
    get_comments,
    get_comment,
    delete_comment,
    update_comment,
)
from dependencies import get_db
from gemini import profanity_checker

router = APIRouter()


@router.post("/comments/", response_model=schemas.Comment)
def create_comment_endpoint(
    comment: schemas.CommentCreate, db: Session = Depends(get_db)
):
    if profanity_checker(comment.content):
        raise HTTPException(status_code=400, detail="The comment contains profanity")
    return create_comment(db, comment)


@router.get("/comments/{comment_id}", response_model=schemas.Comment)
def get_comment_endpoint(comment_id: int, db: Session = Depends(get_db)):
    db_comment = get_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.get("/comments/", response_model=list[schemas.Comment])
def get_comments_endpoint(
    post_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return get_comments(db, post_id, skip=skip, limit=limit)


@router.put("/comments/{comment_id}", response_model=schemas.Comment)
def update_comment_endpoint(
    comment_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)
):
    db_comment = update_comment(db, comment_id, comment)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if profanity_checker(comment.content):
        raise HTTPException(status_code=400, detail="The comment contains profanity")
    return db_comment


@router.delete("/comments/{comment_id}", response_model=schemas.Comment)
def delete_comment_endpoint(comment_id: int, db: Session = Depends(get_db)):
    db_comment = delete_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment
