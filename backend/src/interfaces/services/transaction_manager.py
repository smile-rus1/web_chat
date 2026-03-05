from typing import Protocol

from src.interfaces.infrastructure.repo.account_repo import IAccountRepo
from src.interfaces.infrastructure.repo.chat_repo import IChatRepo
from src.interfaces.infrastructure.repo.contact_repo import IContactRepo


class IBaseTransactionManager(Protocol):
    account_repo: IAccountRepo
    chat_repo: IChatRepo
    contact_repo: IContactRepo

    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError
