from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatPreview:
    chat_id: int
    created_at: datetime
    participants: list["ChatPreviewParticipant"]
    last_message: str | None


@dataclass
class ChatPreviewParticipant:
    account_id: int
    username: str
    first_name: str
    last_name: str
    phone_number: str
    avatar_url: str | None
