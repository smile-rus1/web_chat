from sqlalchemy import select, asc, or_

from src.infrastructure.db.models import AccountDB


class AccountQueryBuilder:
    def __init__(self):
        self._query = None
        self._filters = []

    def get_query(
            self,
            account_id: int,
            username: str | None,
            phone_number: str | None,
            offset: int | None = None,
            limit: int | None = None
    ):
        return (
            self._select(account_id,offset, limit)
            ._with_username(username)
            ._with_phone_number(phone_number)
            ._apply_filters()
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
            select(AccountDB)
            .where(AccountDB.account_id != account_id)
            .order_by(asc(AccountDB.username))
            .limit(limit)
            .offset(offset)
        )

        return self

    def _with_username(self, username: str | None):
        if username is not None:
            self._filters.append(
                AccountDB.username.like(f"%{username}%")
            )
        return self

    def _with_phone_number(self, phone_number: str | None):
        if phone_number is not None:
            self._filters.append(
                AccountDB.phone_number.like(f"%{phone_number}%")
            )
        return self

    def _apply_filters(self):
        if self._filters:
            self._query = self._query.where(or_(*self._filters))
        return self
