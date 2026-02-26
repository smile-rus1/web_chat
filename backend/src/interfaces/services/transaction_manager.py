from typing import Protocol

from src.interfaces.infrastructure.repo.account_repo import IAccountRepo
from src.interfaces.infrastructure.repo.chat_repo import IChatRepo


class IBaseTransactionManager(Protocol):
    account_repo: IAccountRepo
    chat_repo: IChatRepo

    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError
