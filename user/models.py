from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from core.database import Base


class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    posts = relationship("DBPost", back_populates="owner")
    comments = relationship("DBComment", back_populates="user")

    auto_reply_enabled = Column(Boolean, default=False)
    reply_delay = Column(Integer, default=5)
