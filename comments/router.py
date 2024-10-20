from _datetime import datetime, timedelta

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from celery_app import auto_reply
from comments import schemas
from comments.crud import (
    create_comment,
    get_comments,
    get_comment,
    delete_comment,
    update_comment,
)
from comments.models import DBComment
from comments.schemas import CommentAnalytics
from dependencies import get_db
from gemini import profanity_checker
from user.models import DBUser

router = APIRouter()


@router.post("/comments/", response_model=schemas.Comment)
def create_comment_endpoint(
    comment: schemas.CommentCreate, db: Session = Depends(get_db)
):
    if profanity_checker(comment.content):
        raise HTTPException(status_code=400, detail="The comment contains profanity")

    user = db.query(DBUser).filter(DBUser.id == comment.user_id).first()
    new_comment = create_comment(db, comment)
    if user and user.auto_reply_enabled:
        auto_reply.apply_async(
            (new_comment.id, comment.post_id, user.id), countdown=user.reply_delay
        )

    return new_comment


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


@router.get("/api/comments-daily-breakdown")
def comments_daily_breakdown(
    date_from: str, date_to: str, db: Session = Depends(get_db)
):
    start_date = datetime.strptime(date_from, "%d-%m-%Y")
    end_date = datetime.strptime(date_to, "%d-%m-%Y")

    analytics = []
    current_date = start_date
    while current_date <= end_date:
        total_comments = (
            db.query(DBComment)
            .filter(
                DBComment.created_at >= current_date,
                DBComment.created_at < current_date + timedelta(days=1),
            )
            .count()
        )
        blocked_comments = (
            db.query(DBComment)
            .filter(
                DBComment.created_at >= current_date,
                DBComment.created_at < current_date + timedelta(days=1),
                # ??? filtration by is_blocked
            )
            .count()
        )

        analytics.append(
            CommentAnalytics(
                date=current_date.strftime("%Y-%m-%d"),
                total_comments=total_comments,
                blocked_comments=blocked_comments,
            )
        )
        current_date += timedelta(days=1)

    return analytics
