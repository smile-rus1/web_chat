import json

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler as fastapi_validation_handler
from pydantic import ValidationError

from src.exceptions.auth import AuthException


async def auth_exception_handler(_, exc: AuthException):
    return JSONResponse(status_code=401, content={"message": exc.message()})


async def validation_exception_handler(_, err: ValidationError | RequestValidationError):
    return JSONResponse(status_code=400, content=json.loads(err.json()))


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return await fastapi_validation_handler(request, exc)
