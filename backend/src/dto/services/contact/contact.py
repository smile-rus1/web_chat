from dataclasses import dataclass
from datetime import datetime

from src.dto.base_dto import BaseDTO


@dataclass
class CreateNewContactDTO(BaseDTO):
    account_id: int
    contact_id: int
    contact_name: str


@dataclass
class UpdateContactDTO(CreateNewContactDTO):
    ...


@dataclass
class ContactDTO(BaseDTO):
    account_id: int
    contact_id: int
    contact_name: str
    added_at: datetime | None


@dataclass
class AccountContactDTO(BaseDTO):
    contact_id: int
    contact_name: str
    username: str
    first_name: str
    last_name: str
    phone_number: str
    country: str
    image_url: str
