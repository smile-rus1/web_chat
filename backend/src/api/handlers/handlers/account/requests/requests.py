from fastapi import Body, UploadFile, File, Form
from pydantic import BaseModel


class CreateAccountRequest(BaseModel):
    username: str = Body(..., embed=True)
    first_name: str = Body(..., embed=True)
    last_name: str = Body(..., embed=True)


class UpdateAccountRequest(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    country: str | None = None
    phone_number: str | None = None
    email: str | None = None
    image_url: UploadFile | None = File(None)


def update_account_request(
        username: str = Form(None),
        first_name: str = Form(None),
        last_name: str = Form(None),
        email: str = Form(None),
        phone_number: str = Form(None),
        country: str = Form(None),
        image: UploadFile | None = File(None)
):
    return UpdateAccountRequest(
        username=username,
        first_name=first_name,
        country=country,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        image_url=image,
    )
