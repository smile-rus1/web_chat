from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageResponse(BaseModel):
    message_id: int
    chat_id: int
    sender_id: int
    message_text: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MessagesEventResponse(BaseModel):
    event: str = "messages"
    messages: list[MessageResponse]


class SendMessageResponse(BaseModel):
    event: str = "new_message"
    message: MessageResponse


class DeleteMessageResponse(BaseModel):
    event: str = "message_deleted"
    message_id: int


class UpdateMessageResponse(BaseModel):
    event: str = "message_updated"
    message: MessageResponse
