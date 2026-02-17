from dataclasses import dataclass

from src.dto.base_dto import BaseDTO


@dataclass
class AccountDTO(BaseDTO):
    username: str
    first_name: str
    last_name: str
    country: str
    phone_number: str
    email: str | None = None
    image_url: str | None = None


@dataclass
class CreateAccountDTO(BaseDTO):
    username: str
    first_name: str
    last_name: str


@dataclass
class UpdateAccountDTO(BaseDTO):
    account_id: int
    updating_account_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    country: str | None = None
    phone_number: str | None = None
    email: str | None = None
    image_url: str | None = None
