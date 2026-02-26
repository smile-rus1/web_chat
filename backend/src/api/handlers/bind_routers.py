from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.api.handlers import (
    account_router,
    auth_router
)
from src.api.handlers.exceptions.common_exc_handlers import (
    auth_exception_handler,
    validation_exception_handler,
    request_validation_exception_handler
)
from src.api.handlers.exceptions import (
    account_exception_handler, chat_exception_handler
)
from src.api.handlers.handlers.chat import chat_router_ws, chat_router

from src.api.web_config import WebConfig
from src.exceptions.auth import AuthException
from src.services.exceptions.acc import BaseServiceAccountExceptions
from src.services.exceptions.chat import BaseServiceChatException


def bind_exceptions_handlers(app: FastAPI):
    app.add_exception_handler(AuthException, auth_exception_handler)  # type: ignore
    app.add_exception_handler(ValidationError, validation_exception_handler)  # type: ignore
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)  # type: ignore

    app.add_exception_handler(BaseServiceAccountExceptions, account_exception_handler)  # type: ignore
    app.add_exception_handler(BaseServiceChatException, chat_exception_handler)  # type: ignore


def bind_routers():
    api_routers = APIRouter()
    api_routers.include_router(account_router)
    api_routers.include_router(auth_router)
    api_routers.include_router(chat_router)
    api_routers.include_router(chat_router_ws)

    return api_routers


def bind_routes(app: FastAPI, config: WebConfig):
    routers = bind_routers()
    app.include_router(routers, prefix=config.api_v1_str)
