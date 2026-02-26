from typing import Annotated

from fastapi import APIRouter, status, Depends, Body

from src.api.handlers.handlers.account.requests.requests import (
    CreateAccountRequest,
    UpdateAccountRequest,
    update_account_request,
    SearchAccountsRequest
)
from src.api.handlers.handlers.account.response.reponse import ResponseAccountVM
from src.api.permissions import login_required
from src.api.providers.abstract.services import account_service_provider, files_work_service_provider
from src.api.providers.auth import TokenAuthDep
from src.dto.services.account.account import CreateAccountDTO, UpdateAccountDTO, SearchAccountDTO
from src.services.services.account.account import AccountService
from src.services.services.files_work.files_work import FilesWorkService


account_router = APIRouter(prefix="/accounts", tags=["Accounts"])


@account_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
async def register(
        phone_number: str = Body(embed=True),
        country: str = Body(embed=True),
        account_service: AccountService = Depends(account_service_provider)
):
    await account_service.register(phone_number, country)

    return {"message": "Confirm the secret code, which send to you phone number"}


@account_router.post(
    "/confirm-register"
)
async def confirm_register(
        secret_code: str = Body(embed=True),
        account_service: AccountService = Depends(account_service_provider)
):
    token = await account_service.confirm_register(secret_code)

    return {"register_token": token}


@account_router.post(
    "/create_account/{token}"
)
async def create_account(
        token: str,
        register_data: CreateAccountRequest,
        account_service: AccountService = Depends(account_service_provider)
):
    account_dto = CreateAccountDTO(
        first_name=register_data.first_name,
        last_name=register_data.last_name,
        username=register_data.username
    )
    account = await account_service.create_account(token, account_dto)

    return account


@account_router.patch(
    "/update_account/{account_id}",
    status_code=status.HTTP_202_ACCEPTED
)
@login_required
async def update_account(
        account_id: int,
        auth: TokenAuthDep,
        update_data: Annotated[UpdateAccountRequest, Depends(update_account_request)],
        account_service: AccountService = Depends(account_service_provider),
        files_work: FilesWorkService = Depends(files_work_service_provider),
):
    image_path = None
    if update_data.image_url is not None:
        image_path = await files_work.upload_image(
            file=update_data.image_url,
            filename=update_data.image_url.filename
        )

    account_dto = UpdateAccountDTO(
        account_id=auth.request.state.user.account_id,
        updating_account_id=account_id,
        username=auth.request.state.user.username,
        first_name=update_data.first_name,
        last_name=update_data.last_name,
        image_url=image_path,
        country=update_data.country,
        phone_number=update_data.phone_number,
        email=update_data.email
    )

    account = await account_service.update_account(account_dto)
    return ResponseAccountVM(
        account_id=account_id,
        username=account.username,
        first_name=account.first_name,
        last_name=account.last_name,
        phone_number=account.phone_number,
        image_url=account.image_url,
        country=account.country,
        email=account.email
    )


@account_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ResponseAccountVM]
)
@login_required
async def search_accounts(
        auth: TokenAuthDep,
        search: SearchAccountsRequest = Depends(),
        account_service: AccountService = Depends(account_service_provider),
):
    search_dto = SearchAccountDTO(
        account_id=auth.request.state.user.account_id,
        username=search.username,
        phone_number=search.phone_number,
        offset=search.offset,
        limit=search.limit
    )
    accounts = await account_service.search_accounts(search_dto)
    models = [
        ResponseAccountVM(
            account_id=model.account_id,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            phone_number=model.phone_number,
            image_url=model.image_url,
            country=model.country,
            email=model.email
        )
        for model in accounts
    ]
    return models


@account_router.get(
    "/{account_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseAccountVM
)
@login_required
async def get_account_by_id(
        account_id: int,
        auth: TokenAuthDep,
        account_service: AccountService = Depends(account_service_provider),
):
    account = await account_service.get_account_by_id(account_id=account_id)
    return ResponseAccountVM(
        account_id=account_id,
        username=account.username,
        first_name=account.first_name,
        last_name=account.last_name,
        phone_number=account.phone_number,
        image_url=account.image_url,
        country=account.country,
        email=account.email
    )


@account_router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@login_required
async def delete_account(
        account_id: int,
        auth: TokenAuthDep,
        account_service: AccountService = Depends(account_service_provider),
):
    await account_service.delete_account(
        auth.request.state.user.account_id,
        account_id
    )
