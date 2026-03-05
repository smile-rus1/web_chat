from src.dto.db.contact.contact import Contact
from src.dto.db.contact.contact_read import AccountContact


class IContactRepo:
    async def add_to_account_contact(self, contact: Contact) -> Contact:
        ...

    async def update_contact_name(self, contact: Contact) -> None:
        ...

    async def delete_contact(self, contact: Contact) -> None:
        ...

    async def get_account_contacts(self, account_id: int) -> list[AccountContact]:
        ...
