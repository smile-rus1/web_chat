from typing import Protocol

from src.interfaces.infrastructure.repo.account_repo import IAccountRepo


class IBaseTransactionManager(Protocol):
    account_repo: IAccountRepo

    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError
