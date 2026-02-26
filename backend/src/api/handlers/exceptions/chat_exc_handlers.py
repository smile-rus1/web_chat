from fastapi.responses import JSONResponse

from src.services.exceptions.chat import (
    BaseServiceChatException,
    ServiceParticipantNotFoundError,
    ChatConstraintViolationExceptionService,
    ServiceDuplicateParticipantError
)


def chat_exception_handler(_, exc: BaseServiceChatException):
    match exc:
        case ServiceParticipantNotFoundError():
            return JSONResponse(status_code=404, content=exc.message())

        case (ChatConstraintViolationExceptionService() | ServiceDuplicateParticipantError()):
            return JSONResponse(status_code=400, content=exc.message())

        case BaseServiceChatException():
            return JSONResponse(status_code=500, content={"message": "Sorry, service not available"})
