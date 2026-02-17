from fastapi import APIRouter, Depends, status, Body

from src.api.providers.abstract import services
from src.api.providers.auth import TokenAuthDep
from src.services.services.account.auth import AuthService


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/check_account_phone",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Not registered"},
        500: {"description": "Internal Server Error"}
    }
)
async def check_account_phone(
        phone_number: str = Body(embed=True),
        auth_service: AuthService = Depends(services.auth_service_provider),
):
    """
    Check account number for authorize
    """
    await auth_service.check_account_phone(phone_number)

    return {"message": "Confirm the secret code, which send to you phone number"}


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Not registered"},
        500: {"description": "Internal Server Error"}
    }
)
async def login_user(
        auth: TokenAuthDep,
        secret_code: str = Body(embed=True),
        auth_service: AuthService = Depends(services.auth_service_provider),
):
    """
    Authorize account
    """
    tokens = await auth_service.authenticate_account(secret_code, auth)

    return tokens


@auth_router.post(
    "/logout",
    status_code=status.HTTP_200_OK
)
async def logout(auth: TokenAuthDep):
    await auth.unset_tokens()
    return {"detail": "Tokens deleted"}


@auth_router.post(
    "/refresh",
    status_code=status.HTTP_200_OK
)
async def refresh_access_token(auth: TokenAuthDep):
    await auth.refresh_access_token()
    return {"detail": "Access token has been refresh"}
