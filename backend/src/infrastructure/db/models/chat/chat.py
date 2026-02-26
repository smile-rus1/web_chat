from src.infrastructure.db.models.base import Base
from datetime import datetime

from sqlalchemy import Integer, DateTime, func, Text, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship


class ChatDB(Base):
    __tablename__ = "chats"

    chat_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    participants_key: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
    messages: Mapped[list["MessageDB"]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )
    participants: Mapped[list["AccountDB"]] = relationship(  # type: ignore
        "AccountDB",
        secondary="chat_participants",
        back_populates="chats"
    )


class ChatParticipantDB(Base):
    __tablename__ = "chat_participants"

    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.chat_id", ondelete="CASCADE"), primary_key=True
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.account_id", ondelete="CASCADE"), primary_key=True
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now()
    )


class MessageDB(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
    message_text: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.chat_id", ondelete="CASCADE"),
        nullable=False
    )
    sender_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.account_id", ondelete="SET NULL"), nullable=True
    )
    chat: Mapped["ChatDB"] = relationship(
        "ChatDB",
        back_populates="messages"
    )
    sender: Mapped["AccountDB"] = relationship("AccountDB")  # type: ignore
