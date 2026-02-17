from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class BaseServiceAccountExceptions(BaseExceptions):
    ...


@dataclass
class AccountAlreadyExistService(BaseServiceAccountExceptions):
    username: str

    def message(self):
        return f"Account with username {self.username} already exist"


@dataclass
class AccountNotFoundByUsernameService(BaseServiceAccountExceptions):
    username: str

    def message(self):
        return f"Account with username {self.username} not found"


@dataclass
class AccountIDExceptionService(BaseServiceAccountExceptions):
    account_id: int


@dataclass
class AccountNotFoundByIDService(AccountIDExceptionService):
    def message(self):
        return f"Account with {self.account_id} id not found!"


class InvalidSecretCode(BaseServiceAccountExceptions):
    def message(self):
        return f"Invalid code!"


@dataclass
class AccountNotFoundByPhoneService(BaseServiceAccountExceptions):
    phone_number: str

    def message(self):
        return f"Account with phone {self.phone_number} id not found!"


@dataclass
class AccountAlreadyExistsWithPhoneNumberService(BaseServiceAccountExceptions):
    phone_number: str

    def message(self):
        return f"Account with {self.phone_number} phone number already exists!"
