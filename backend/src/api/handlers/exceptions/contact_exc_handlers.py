from fastapi.responses import JSONResponse

from src.services.exceptions.contact import (
    BaseServiceContactException,
    NotFoundContactByID, DuplicateAddedAccountToContact,
    AccessDeniedToAddedContact
)


def contact_exception_handler(_, exc: BaseServiceContactException):
    match exc:
        case (DuplicateAddedAccountToContact() | AccessDeniedToAddedContact()):
            return JSONResponse(status_code=400, content=exc.message())

        case NotFoundContactByID():
            return JSONResponse(status_code=404, content=exc.message())

        case BaseServiceContactException():
            return JSONResponse(status_code=500, content={"message": "Sorry, service not available"})
