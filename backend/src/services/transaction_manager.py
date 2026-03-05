from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces.infrastructure.repo.account_repo import IAccountRepo
from src.interfaces.infrastructure.repo.chat_repo import IChatRepo
from src.interfaces.infrastructure.repo.contact_repo import IContactRepo
from src.interfaces.services.transaction_manager import IBaseTransactionManager


class BaseTransactionManager(IBaseTransactionManager):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


class TransactionManager(BaseTransactionManager):
    def __init__(
            self,
            session: AsyncSession,
            account_repo: Type[IAccountRepo],
            chat_repo: Type[IChatRepo],
            contact_repo: Type[IContactRepo]
    ):
        super().__init__(session=session)
        self.account_repo = account_repo(session=session)  # type: ignore
        self.chat_repo = chat_repo(session=session)  # type: ignore
        self.contact_repo = contact_repo(session=session)  # type: ignore
