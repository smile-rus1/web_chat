from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseServiceChatException(BaseExceptions):
    pass


@dataclass
class ServiceParticipantNotFoundError(BaseServiceChatException):
    def message(self):
        return f"One or more participants do not exist."


@dataclass
class ServiceDuplicateParticipantError(BaseServiceChatException):
    def message(self):
        return f'The current chat contains duplicate participant'


@dataclass
class ChatConstraintViolationExceptionService(BaseServiceChatException):
    def message(self):
        return f'You cannot create this chat'

