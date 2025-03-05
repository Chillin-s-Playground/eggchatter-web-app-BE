from datetime import datetime, timezone

from pydantic import Base
from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr


class CommonFields(Base):
    """공통 필드 클래스"""

    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now(), nullable=False, index=True)
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    )
