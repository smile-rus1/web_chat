from pydantic import BaseModel


class CreateNewContactVM(BaseModel):
    contact_id: int
    contact_name: str
