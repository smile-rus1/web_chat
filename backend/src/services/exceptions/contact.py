from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseServiceContactException(BaseExceptions):
    pass


@dataclass
class NotFoundContactByID(BaseServiceContactException):
    contact_id: int

    def message(self):
        return f"Contact with contact_id: {self.contact_id} not found!"


@dataclass
class DuplicateAddedAccountToContact(BaseServiceContactException):
    contact_id: int

    def message(self):
        return f"This contact {self.contact_id} already added to your contacts!"


@dataclass
class AccessDeniedToAddedContact(BaseServiceContactException):
    contact_id: int

    def message(self):
        return f"You cannot add {self.contact_id} to your contacts!"
