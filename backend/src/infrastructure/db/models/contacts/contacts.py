from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.models.base import Base


class ContactDB(Base):
    __tablename__ = "contacts"

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.account_id", ondelete="CASCADE"), primary_key=True
    )
    contact_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.account_id", ondelete="CASCADE"), primary_key=True
    )
    contact_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    added_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now()
    )
