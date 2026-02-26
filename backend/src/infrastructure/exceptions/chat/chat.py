from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseChatException(BaseExceptions):
    ...


@dataclass
class ChatParticipantNotFound(BaseChatException):
    def message(self):
        return f"One or more participants do not exist."


@dataclass
class DuplicateChatParticipant(BaseChatException):
    def message(self):
        return f"Duplicate participant detected in chat creation in chat"


@dataclass
class ChatConstraintViolation(BaseChatException):
    def message(self):
        return f"Null value violation while creating chat"
