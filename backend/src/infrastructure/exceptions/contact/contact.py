from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseContactException(BaseExceptions):
    ...


@dataclass
class ContactNotFoundByID(BaseContactException):
    contact_id: int

    def message(self):
        return f"Contact with contact_id: {self.contact_id} not found!"


@dataclass
class DuplicateContactAccount(BaseContactException):
    contact_id: int

    def message(self):
        return f"This contact {self.contact_id} already added to your contacts!"
