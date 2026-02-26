from dataclasses import asdict

from loguru import logger
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dto.db.account.account import Account
from src.infrastructure.db.models import AccountDB
from src.infrastructure.db.repo.account_repo.query import AccountQueryBuilder
from src.infrastructure.exceptions.account.account import (
    AccountAlreadyExist,
    AccountNotFoundByPhone,
    AccountAlreadyExistsWithPhone,
    BaseAccountException,
    AccountNotFoundByUsername,
    AccountNotFoundByID
)
from src.interfaces.infrastructure.repo.account_repo import IAccountRepo
from src.interfaces.infrastructure.sqlalchemy_repo import SqlAlchemyDAO


class AccountRepo(SqlAlchemyDAO, IAccountRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self._query_builder = AccountQueryBuilder()

    async def get_account_by_id(self, account_id: int) -> Account:
        account_sql = select(AccountDB).where(AccountDB.account_id == account_id)
        res = (await self._session.execute(account_sql)).scalar_one_or_none()

        if res is None:
            raise AccountNotFoundByID(account_id)

        return Account(
            account_id=res.account_id,
            phone_number=res.phone_number,
            first_name=res.first_name,
            last_name=res.last_name,
            username=res.username,
            country=res.country,
            email=res.email,
            is_admin=res.is_admin,
            is_superuser=res.is_superuser,
            image_url=res.image_url
        )

    async def get_account_by_phone(self, phone_number: str) -> Account:
        account_sql = select(AccountDB).where(AccountDB.phone_number == phone_number)
        res = (await self._session.execute(account_sql)).scalar_one_or_none()

        if res is None:
            raise AccountNotFoundByPhone(phone_number)

        return Account(
            account_id=res.account_id,
            phone_number=res.phone_number,
            first_name=res.first_name,
            last_name=res.last_name,
            username=res.username,
            country=res.country,
            email=res.email,
            is_admin=res.is_admin,
            is_superuser=res.is_superuser
        )

    async def get_account_by_username(self, username: str) -> Account:
        account_sql = select(AccountDB).where(AccountDB.username == username)
        res = (await self._session.execute(account_sql)).scalar_one_or_none()

        if res is None:
            raise AccountNotFoundByUsername(username)

        return Account(
            account_id=res.account_id,
            phone_number=res.phone_number,
            first_name=res.first_name,
            last_name=res.last_name,
            username=res.username,
            country=res.country,
            email=res.email,
            is_admin=res.is_admin,
            is_superuser=res.is_superuser
        )

    async def create_account(self, account: Account) -> Account:
        account_sql = (
            insert(AccountDB)
            .values(
                username=account.username,
                phone_number=account.phone_number,
                first_name=account.first_name,
                last_name=account.last_name,
                country=account.country
            )
            .returning(AccountDB.account_id)
        )

        try:
            result = await self._session.execute(account_sql)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{AccountRepo.__name__} in {self.create_account.__name__}"
            ).error(f"WITH DATA {account}\nMESSAGE: {exc}")
            raise self._error_parser(account, exc)

        account_id = result.scalar_one()
        account.account_id = account_id
        return account

    async def update_account(self, account: Account) -> None:
        data = asdict(account)
        account_fields = {
            k: v for k, v in data.items() if v is not None and v != "" and k not in {"account_id"}
        }

        update_sql = (
            update(AccountDB)
            .where(
                AccountDB.account_id == account.account_id
            )
            .values(**account_fields)
        )
        try:
            await self._session.execute(update_sql)
        except IntegrityError as exc:
            logger.bind(
                app_name=f"{AccountRepo.__name__} in {self.update_account.__name__}"
            ).error(f"WITH DATA {account}\nMESSAGE: {exc}")
            raise self._error_parser(account, exc)

    async def delete_account(self, account_id: int) -> None:
        sql = delete(AccountDB).where(AccountDB.account_id == account_id)
        await self._session.execute(sql)

    async def search_accounts(self, account: Account, offset: int, limit: int) -> list[Account]:
        sql = self._query_builder.get_query(
            account_id=account.account_id,
            username=account.username,
            phone_number=account.phone_number,
            offset=offset,
            limit=limit
        )

        result = await self._session.execute(sql)
        models = result.scalars().all()

        return [
            Account(
                account_id=acc.account_id,
                phone_number=acc.phone_number,
                first_name=acc.first_name,
                last_name=acc.last_name,
                username=acc.username,
                country=acc.country,
                email=acc.email,
                image_url=acc.image_url,
            )
            for acc in models
        ]

    @staticmethod
    def _error_parser(
            account: Account,
            exc: IntegrityError
    ) -> BaseAccountException:
        database_column = exc.__cause__.__cause__.constraint_name  # type: ignore
        if database_column == "accounts_username_key":
            return AccountAlreadyExist(account.username)

        if database_column == "accounts_phone_number_key":
            return AccountAlreadyExistsWithPhone(account.username)
