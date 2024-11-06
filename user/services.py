from sqlalchemy.orm import Session

from user.models import DBUser


def toggle_auto_reply(db: Session, user: DBUser) -> DBUser:
    user.auto_reply_enabled = not user.auto_reply_enabled
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
