from src.dto.db.account.account import Account


class IAccountRepo:
    async def create_account(self, account: Account) -> Account:
        raise NotImplementedError

    async def update_account(self, account: Account) -> None:
        raise NotImplementedError

    async def get_account_by_phone(self, phone_number: str) -> Account:
        raise NotImplementedError

    async def get_account_by_id(self, account_id: int) -> Account:
        raise NotImplementedError

    async def get_account_by_username(self, username: str) -> Account:
        raise NotImplementedError

    async def delete_account(self, account_id: int) -> None:
        raise NotImplementedError

    async def search_accounts(self, account: Account, offset: int, limit: int) -> list[Account]:
        raise NotImplementedError
