from fastapi import WebSocket
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from fastapi import Request

from src.api.providers.auth import get_jwt_token_auth
from src.core.config_reader import config
from src.dto.web.auth import AnonymousUser, ActiveUser


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware that injects the authenticated user into `request.state.user`.
    If no valid access token is found, the user is treated as anonymous.
    """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint,
    ) -> Response:
        jwt_auth = await get_jwt_token_auth(request=request)
        access_token_data = await jwt_auth.read_token(config.auth.access_token_name)

        if access_token_data is None:
            request.state.user = AnonymousUser()
        else:
            request.state.user = ActiveUser(
                account_id=access_token_data.get("account_id"),
                username=access_token_data.get("username"),
                first_name=access_token_data.get("first_name"),
                last_name=access_token_data.get("last_name"),
                email=access_token_data.get("email"),
                is_admin=access_token_data.get("is_admin"),
                is_superuser=access_token_data.get("is_superuser"),
            )
        response = await call_next(request)
        return response


async def get_auth_websocket(ws: WebSocket):
    jwt_auth = await get_jwt_token_auth(request=ws)
    access_token_data = await jwt_auth.read_token(config.auth.access_token_name)

    if access_token_data is None:
        return AnonymousUser()

    return ActiveUser(
        account_id=access_token_data.get("account_id"),
        username=access_token_data.get("username"),
        first_name=access_token_data.get("first_name"),
        last_name=access_token_data.get("last_name"),
        email=access_token_data.get("email"),
        is_admin=access_token_data.get("is_admin"),
        is_superuser=access_token_data.get("is_superuser"),
    )
