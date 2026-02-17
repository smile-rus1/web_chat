from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseAccountException(BaseExceptions):
    ...


@dataclass
class AccountAlreadyExist(BaseAccountException):
    username: str

    def message(self):
        return f"Account with username {self.username} already exist"


@dataclass
class AccountNotFoundByUsername(BaseAccountException):
    username: str

    def message(self):
        return f"Account with username {self.username} not found"


@dataclass
class AccountIDException(BaseAccountException):
    account_id: int


@dataclass
class AccountNotFoundByID(AccountIDException):
    def message(self):
        return f"Account with {self.account_id} id not found!"


@dataclass
class AccountNotFoundByPhone(BaseAccountException):
    phone_number: str

    def message(self):
        return f"Account with phone {self.phone_number} id not found!"


@dataclass
class InvalidSecretCode(BaseAccountException):
    def message(self):
        return f"Invalid secret code!"


@dataclass
class AccountAlreadyExistsWithPhone(BaseAccountException):
    phone_number: str

    def message(self):
        return f"Account with {self.phone_number} phone number already exists!"
