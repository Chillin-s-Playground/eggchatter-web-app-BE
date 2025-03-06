from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CommonFields(Base):
    """공통 필드 클래스 (SQLAlchemy ORM)"""

    __abstract__ = True  # SQLAlchemy에서 추상 클래스 설정

    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
