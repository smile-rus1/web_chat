from loguru import logger
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dto.db.account.account import Account
from src.dto.db.contact.contact import Contact
from src.dto.db.contact.contact_read import AccountContact
from src.infrastructure.db.models import ContactDB
from src.infrastructure.db.repo.contact_repo.query import ContactQueryBuilder
from src.infrastructure.exceptions.contact.contact import (
    BaseContactException,
    ContactNotFoundByID,
    DuplicateContactAccount
)
from src.interfaces.infrastructure.repo.contact_repo import IContactRepo
from src.interfaces.infrastructure.sqlalchemy_repo import SqlAlchemyRepo


class ContactRepo(SqlAlchemyRepo, IContactRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self._query_builder = ContactQueryBuilder()

    async def add_to_account_contact(self, contact: Contact) -> Contact:
        sql = (
            insert(ContactDB)
            .values(
                account_id=contact.account_id,
                contact_id=contact.contact_id,
                contact_name=contact.contact_name
            )
            .returning(ContactDB.added_at)
        )
        try:
            result = await self._session.execute(sql)
        except IntegrityError as exc:
            logger.bind(
                app_name=f"{ContactRepo.__name__} in {self.add_to_account_contact.__name__}"
            ).error(f"WITH DATA {contact}\nMESSAGE: {exc}")
            raise self._error_parser(exc, contact)
        date = result.scalar_one()
        contact.added_at = date
        return contact

    async def update_contact_name(self, contact: Contact) -> None:
        sql = (
            update(ContactDB)
            .where(
                ContactDB.contact_id == contact.contact_id,
                ContactDB.account_id == contact.account_id
            )
            .values(
                contact_name=contact.contact_name
            )
        )
        try:
            await self._session.execute(sql)
        except IntegrityError as exc:
            logger.bind(
                app_name=f"{ContactRepo.__name__} in {self.update_contact_name.__name__}"
            ).error(f"WITH DATA {contact}\nMESSAGE: {exc}")
            raise self._error_parser(exc, contact)

    async def delete_contact(self, contact: Contact) -> None:
        sql = (
            delete(ContactDB)
            .where(
                ContactDB.contact_id == contact.contact_id,
                ContactDB.account_id == contact.account_id
            )
        )
        await self._session.execute(sql)

    async def get_account_contacts(self, account_id: int) -> list[AccountContact]:
        sql = self._query_builder.get_query(account_id)
        res = (await self._session.execute(sql)).all()
        contacts = [
            AccountContact(
                contact_id=row.contact_id,
                contact_name=row.contact_name,
                account=Account(
                    username=row.username,
                    first_name=row.first_name,
                    last_name=row.last_name,
                    phone_number=row.phone_number,
                    country=row.country,
                    image_url=row.image_url,
                )
            )
            for row in res
        ]
        return contacts

    @staticmethod
    def _error_parser(
            exc: IntegrityError,
            contact: Contact
    ) -> BaseContactException:
        error_message = str(exc).lower()

        if "contacts_contact_id_fkey" in error_message:
            return ContactNotFoundByID(contact.contact_id)

        elif "duplicate key value violates unique constraint" in error_message:
            return DuplicateContactAccount(contact.contact_id)

        return BaseContactException()
