from functools import wraps

from fastapi import HTTPException, status


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
