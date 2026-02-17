from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.db.models.base import Base


class AccountDB(Base):
    __tablename__ = "accounts"

    account_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True
    )
    phone_number: Mapped[str] = mapped_column(
        String(13),
        unique=True,
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(30),
        nullable=True
    )
    country: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
