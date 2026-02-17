from fastapi.responses import JSONResponse

from src.services.exceptions.acc import (
    BaseServiceAccountExceptions,
    AccountAlreadyExistService,
    AccountNotFoundByUsernameService,
    AccountNotFoundByPhoneService,
    AccountAlreadyExistsWithPhoneNumberService,
    InvalidSecretCode, AccountNotFoundByIDService
)


def account_exception_handler(_, exc: BaseServiceAccountExceptions):
    match exc:
        case (AccountAlreadyExistService() | AccountAlreadyExistsWithPhoneNumberService()):
            return JSONResponse(status_code=409, content={"message": exc.message()})

        case (AccountNotFoundByUsernameService() | AccountNotFoundByPhoneService() | AccountNotFoundByIDService()):
            return JSONResponse(status_code=404, content={"message": exc.message()})

        case InvalidSecretCode():
            return JSONResponse(status_code=400, content={"message": exc.message()})

        case BaseServiceAccountExceptions():
            return JSONResponse(status_code=500, content={"message": "Sorry, service not available"})
