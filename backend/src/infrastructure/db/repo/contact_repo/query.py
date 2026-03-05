from sqlalchemy import select, asc

from src.infrastructure.db.models import ContactDB, AccountDB


class ContactQueryBuilder:
    def __init__(self):
        self._query = None

    def get_query(
            self,
            account_id: int,
            offset: int | None = None,
            limit: int | None = None,
    ):
        return (
            self._select(account_id, offset, limit)
            ._build()
        )

    def _build(self):
        return self._query

    def _select(
            self,
            account_id: int,
            offset: int | None = None,
            limit: int | None = None
    ):
        self._query = (
            select(
                ContactDB.contact_id,
                ContactDB.contact_name,
                AccountDB.username,
                AccountDB.first_name,
                AccountDB.last_name,
                AccountDB.phone_number,
                AccountDB.country,
                AccountDB.image_url
            )
            .join(AccountDB, AccountDB.account_id == ContactDB.contact_id)
            .where(ContactDB.account_id == account_id)
            .order_by(asc(ContactDB.contact_name))
            .limit(limit)
            .offset(offset)
        )

        return self
