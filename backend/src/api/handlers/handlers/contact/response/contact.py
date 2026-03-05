from pydantic import BaseModel


class AccountContactVM(BaseModel):
    contact_id: int
    contact_name: str
    username: str
    first_name: str | None
    last_name: str | None
    phone_number: str | None
    country: str | None
    image_url: str | None
