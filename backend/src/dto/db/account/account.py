from dataclasses import dataclass
from datetime import datetime


@dataclass
class Account:
    account_id: int | None = None
    username: str | None = None
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    is_superuser: bool | None = None
    is_admin: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    image_url: str | None = None
    country: str | None = None
