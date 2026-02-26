from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatParticipant:
    chat_id: int | None = None
    account_id: int | None = None
    joined_at: datetime | None = None


@dataclass
class Message:
    message_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    message_text: str | None = None
    chat_id: int | None = None
    sender_id: int | None = None


@dataclass
class Chat:
    chat_id: int | None = None
    created_at: datetime | None = None
    participants: list[ChatParticipant] | None = None
    messages: list[Message] | None = None

