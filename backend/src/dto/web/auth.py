from pydantic import BaseModel


class AnonymousUser(BaseModel):
    account_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    is_admin: bool | None = None
    is_superuser: bool | None = None


class ActiveUser(BaseModel):
    account_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    is_admin: bool | None = None
    is_superuser: bool | None = None
