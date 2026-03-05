from dataclasses import dataclass


@dataclass
class Contact:
    account_id: int | None = None
    contact_id: int | None = None
    contact_name: str | None = None
    added_at: str | None = None
