from pydantic import BaseModel


class ResponseAccountVM(BaseModel):
    account_id: int
    username: str
    first_name: str
    last_name: str
    phone_number: str
    country: str | None = None
    email: str | None = None
    image_url: str | None = None
