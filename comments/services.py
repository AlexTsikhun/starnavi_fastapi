from sqlalchemy import func, case
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from comments import schemas
from comments.models import DBComment


def get_comments_daily_breakdown(
    db: Session, start_date: datetime, end_date: datetime
) -> List[schemas.CommentAnalytics]:
    results = (
        db.query(
            func.date(DBComment.created_at).label("date"),
            func.count(DBComment.id).label("total_comments"),
            func.count(
                case(
                    (
                        DBComment.is_blocked == 1,
                        1,
                    ),
                    else_=None,
                )
            ).label("blocked_comments"),
        )
        .filter(DBComment.created_at >= start_date, DBComment.created_at <= end_date)
        .group_by(func.date(DBComment.created_at))
        .order_by(func.date(DBComment.created_at))
        .all()
    )

    return [
        schemas.CommentAnalytics(
            date=datetime.strptime(row.date, "%Y-%m-%d").strftime("%Y-%m-%d"),
            total_comments=row.total_comments,
            blocked_comments=row.blocked_comments,
        )
        for row in results
    ]
