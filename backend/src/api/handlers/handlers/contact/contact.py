from dataclasses import asdict

from fastapi import APIRouter, status, Depends

from src.api.handlers.handlers.contact.requests.requests import CreateNewContactVM
from src.api.handlers.handlers.contact.response.contact import AccountContactVM
from src.api.permissions import login_required
from src.api.providers.abstract.services import contact_service_provider
from src.api.providers.auth import TokenAuthDep
from src.dto.services.contact.contact import CreateNewContactDTO, UpdateContactDTO
from src.services.services.contact.contact import ContactService


contact_router = APIRouter(prefix="/contacts", tags=["Contacts"])


@contact_router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
@login_required
async def create_new_contact(
        auth: TokenAuthDep,
        contact: CreateNewContactVM,
        contact_service: ContactService = Depends(contact_service_provider)
):
    contact_dto = CreateNewContactDTO(
        contact_id=contact.contact_id,
        account_id=auth.request.state.user.account_id,
        contact_name=contact.contact_name
    )
    new_contact = await contact_service.create_new_contact(contact_dto)

    return new_contact


@contact_router.patch(
    "/update_contact_name",
    status_code=status.HTTP_202_ACCEPTED
)
@login_required
async def update_contact_name(
        auth: TokenAuthDep,
        contact: CreateNewContactVM,
        contact_service: ContactService = Depends(contact_service_provider)
):
    contact_dto = UpdateContactDTO(
        contact_id=contact.contact_id,
        account_id=auth.request.state.user.account_id,
        contact_name=contact.contact_name
    )
    await contact_service.change_contact_name(contact_dto)
    return contact_dto


@contact_router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@login_required
async def delete_contact_from_contacts(
        contact_id: int,
        auth: TokenAuthDep,
        contact_service: ContactService = Depends(contact_service_provider)
):
    await contact_service.delete_contact(
        contact_id=contact_id,
        account_id=auth.request.state.user.account_id
    )


@contact_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[AccountContactVM]
)
async def get_all_contacts_account(
        auth: TokenAuthDep,
        contact_service: ContactService = Depends(contact_service_provider)
):
    contacts = await contact_service.get_all_contacts(auth.request.state.user.account_id)
    contacts = [AccountContactVM.model_validate(asdict(contact)) for contact in contacts]
    return contacts
