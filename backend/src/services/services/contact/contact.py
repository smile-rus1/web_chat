import json
from abc import ABC
from dataclasses import asdict

from loguru import logger

from src.dto.db.contact.contact import Contact
from src.dto.services.contact.contact import CreateNewContactDTO, ContactDTO, UpdateContactDTO, AccountContactDTO
from src.infrastructure.exceptions.contact.contact import BaseContactException, ContactNotFoundByID, \
    DuplicateContactAccount
from src.interfaces.infrastructure.redis_db import IRedisDB
from src.interfaces.services.transaction_manager import IBaseTransactionManager
from src.services.exceptions.contact import NotFoundContactByID, BaseServiceContactException, \
    DuplicateAddedAccountToContact, AccessDeniedToAddedContact


class ContactUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm


class CreateNewContact(ContactUseCase):
    async def __call__(self, contact_dto: CreateNewContactDTO) -> ContactDTO:
        if contact_dto.contact_id == contact_dto.account_id:
            raise AccessDeniedToAddedContact(contact_dto.contact_id)

        contact = Contact(
            contact_id=contact_dto.contact_id,
            account_id=contact_dto.account_id,
            contact_name=contact_dto.contact_name
        )
        try:
            res = await self._tm.contact_repo.add_to_account_contact(contact)
            await self._tm.commit()

        except BaseContactException as exc:
            logger.bind(
                app_name=f"{CreateNewContactDTO.__name__}"
            ).error(f"WITH DATA {contact}\nMESSAGE: {exc}")
            await self._tm.rollback()

            match exc:
                case ContactNotFoundByID():
                    raise NotFoundContactByID(contact_dto.contact_id)

                case DuplicateContactAccount():
                    raise DuplicateAddedAccountToContact(contact_dto.contact_id)

                case _:
                    raise BaseServiceContactException()

        return ContactDTO(
            account_id=contact_dto.account_id,
            contact_id=contact_dto.contact_id,
            contact_name=contact_dto.contact_name,
            added_at=res.added_at
        )


class UpdateContactName(ContactUseCase):
    async def __call__(self, contact_dto: UpdateContactDTO) -> None:
        contact = Contact(
            contact_id=contact_dto.contact_id,
            account_id=contact_dto.account_id,
            contact_name=contact_dto.contact_name
        )
        try:
            await self._tm.contact_repo.update_contact_name(contact)
            await self._tm.commit()

        except BaseContactException as exc:
            logger.bind(
                app_name=f"{CreateNewContactDTO.__name__}"
            ).error(f"WITH DATA {contact}\nMESSAGE: {exc}")
            await self._tm.rollback()


class DeleteContact(ContactUseCase):
    async def __call__(self, contact_id: int, account_id: int) -> None:
        contact = Contact(
            contact_id=contact_id,
            account_id=account_id
        )
        await self._tm.contact_repo.delete_contact(contact)
        await self._tm.commit()


class GetAllContactsAccount(ContactUseCase):
    async def __call__(self, account_id: int, redis_db: IRedisDB) -> list[AccountContactDTO]:
        key = f"contacts_account_{account_id}"
        cached = await redis_db.get(key)
        if cached is None:
            contacts = await self._tm.contact_repo.get_account_contacts(account_id)
            contacts = [asdict(contact) for contact in contacts]
            await redis_db.set(key, json.dumps(contacts), expire=600)
        else:
            contacts = json.loads(cached)

        dtos = [
            AccountContactDTO(
                contact_id=data.get("contact_id"),
                contact_name=data.get("contact_name"),
                username=data.get("account").get("username"),
                first_name=data.get("account").get("first_name"),
                last_name=data.get("account").get("last_name"),
                phone_number=data.get("account").get("phone_number"),
                country=data.get("account").get("country"),
                image_url=data.get("account").get("image_url"),
            )
            for data in contacts
        ]
        return dtos


class ContactService:
    def __init__(
            self,
            tm: IBaseTransactionManager,
            redis_db: IRedisDB
    ):
        self._tm = tm
        self._redis_db = redis_db

    async def create_new_contact(self, contact_dto: CreateNewContactDTO) -> ContactDTO:
        return await CreateNewContact(self._tm)(contact_dto)

    async def change_contact_name(self, contact_dto: UpdateContactDTO) -> None:
        return await UpdateContactName(self._tm)(contact_dto)

    async def delete_contact(self, contact_id: int, account_id: int) -> None:
        return await DeleteContact(self._tm)(contact_id, account_id)

    async def get_all_contacts(self, account_id: int) -> list[AccountContactDTO]:
        return await GetAllContactsAccount(self._tm)(account_id, self._redis_db)
