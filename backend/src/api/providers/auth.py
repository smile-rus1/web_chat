from typing import Annotated

from fastapi import Depends

from starlette.requests import HTTPConnection
from starlette.responses import Response

from src.api.auth_jwt import JWTAuth
from src.interfaces.web.auth import IJWTAuth


async def get_jwt_token_auth(request: HTTPConnection = None, response: Response = None) -> JWTAuth:
    return JWTAuth(request=request, response=response)


TokenAuthDep = Annotated[IJWTAuth, Depends(get_jwt_token_auth)]
