from dataclasses import dataclass

from src.dto.db.account.account import Account


@dataclass
class AccountContact:
    contact_id: int
    contact_name: str
    account: Account
