from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database import SessionLocal, Base, engine


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
