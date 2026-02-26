from dataclasses import dataclass
from datetime import datetime

from src.dto.base_dto import BaseDTO


@dataclass
class CreateChatWithUserDTO(BaseDTO):
    participants_ids: list[int]


@dataclass
class ChatParticipantDTO(BaseDTO):
    chat_id: int | None = None
    account_id: int | None = None
    joined_at: datetime | None = None


@dataclass
class ChatMessagesDTO(BaseDTO):
    message_id: int
    chat_id: int
    sender_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    message_text: str | None = None


@dataclass
class ChatDTO(BaseDTO):
    chat_id: int
    created_at: datetime | None
    participants: list[ChatParticipantDTO] | None
    messages: list[ChatMessagesDTO] | None


@dataclass
class SendMessageDTO(BaseDTO):
    sender_id: int
    chat_id: int
    message_text: str


@dataclass
class MessageDTO(BaseDTO):
    message_id: int
    sender_id: int
    chat_id: int
    message_text: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class UpdateMessageDTO(BaseDTO):
    message_id: int
    sender_id: int
    chat_id: int
    old_message_text: str
    new_message_text: str
