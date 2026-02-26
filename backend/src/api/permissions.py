from functools import wraps

from fastapi import HTTPException, status, WebSocket

from src.api.middleware.auth import get_auth_websocket


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        auth = kwargs.get("auth")
        if auth is None:
            for arg in args:
                if hasattr(arg, "request"):
                    auth = arg
                    break
        if auth is None or getattr(auth.request.state.user, "account_id", None) is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        return await func(*args, **kwargs)
    return wrapper


def ws_login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        websocket = kwargs.get("ws") or next(
            (arg for arg in args if isinstance(arg, WebSocket)), None
        )
        if websocket is None:
            raise HTTPException(
                status_code=status.WS_1002_PROTOCOL_ERROR,
                detail="WebSocket protocol needed!"
            )

        account = await get_auth_websocket(websocket)
        if account is None or getattr(account, "account_id", None) is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        websocket.scope["state"] = account
        return await func(*args, **kwargs)
    return wrapper

