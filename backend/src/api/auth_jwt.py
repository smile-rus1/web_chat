from datetime import timedelta, datetime, timezone
from typing import Any

from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError

from starlette.requests import Request
from starlette.responses import Response

from src.core.config_reader import config
from src.exceptions.auth import RefreshTokenNotValid
from src.interfaces.web.auth import IJWTProvider, IJWTAuth


class JWTProvider(IJWTProvider):
    def _encode_jwt(self, data: dict | Any, expires_delta: int) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
        to_encode.update({"exp": expire})
        encoded_token = jwt.encode(to_encode, config.auth.secret_key, algorithm=config.auth.algorithm)
        return encoded_token

    def create_access_token(
            self,
            data: dict | Any,
            expires_delta: int | None = config.auth.access_token_expire
    ) -> str:
        return self._encode_jwt(
            data=data,
            expires_delta=expires_delta
        )

    def create_refresh_token(
            self,
            data: dict | Any,
            expires_delta: int | None = config.auth.refresh_token_expire
    ) -> str:
        return self._encode_jwt(
            data=data,
            expires_delta=expires_delta
        )

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, key=config.auth.secret_key, algorithms=config.auth.algorithm)

        except (JWTError, ValidationError) as exc:
            raise exc

        return payload

    def read_token(self, token: str | None) -> dict | None:
        if token is None:
            return

        try:
            payload = self.decode_token(token)
            account_id = payload.get("account_id")
            if account_id is None:
                return

        except (JWTError, ValidationError):
            return
        return payload


class JWTAuth(IJWTAuth):
    def __init__(
        self,
        request: Request | None = None,
        response: Response | None = None
    ):
        self.request = request
        self.response = response
        self._jwt_provider = JWTProvider()

    async def set_tokens(self, account: dict) -> dict:
        data = {
            "account_id": account.get("account_id"),
            "username": account.get("username"),
            "phone_number": account.get("phone_number"),
            "email": account.get("email"),
            "first_name": account.get("first_name"),
            "last_name": account.get("last_name"),
            "is_admin": account.get("is_admin"),
            "is_superuser": account.get("is_superuser")
        }

        access_token = self._jwt_provider.create_access_token(data)
        refresh_token = self._jwt_provider.create_refresh_token(data)

        await self.set_token(token=access_token, token_type=config.auth.access_token_name)
        await self.set_token(token=refresh_token, token_type=config.auth.refresh_token_name)

        return {"access_token": access_token, "refresh_token": refresh_token}

    async def set_token(self, token: str, token_type: str) -> None:
        if token_type == config.auth.refresh_token_name:
            self.response.set_cookie(key=token_type, value=token, httponly=True, secure=True)
        else:
            self.response.set_cookie(key=token_type, value=token, secure=True)

    async def _get_token(self, token_name: str):
        return self.request.cookies.get(token_name, "")

    async def read_token(self, token_type: str) -> dict | None:
        token = ""
        if token_type == config.auth.access_token_name:
            token = await self._get_token(config.auth.access_token_name)
        elif token_type == config.auth.refresh_token_name:
            token = await self._get_token(config.auth.refresh_token_name)

        token_data = self._jwt_provider.read_token(token)
        return token_data

    async def unset_tokens(self):
        self.response.delete_cookie(config.auth.access_token_name)
        self.response.delete_cookie(config.auth.refresh_token_name)

    async def refresh_access_token(self) -> None:
        refresh_token_data = await self.read_token(config.auth.refresh_token_name)
        if refresh_token_data is None:
            raise RefreshTokenNotValid()

        access_token = self._jwt_provider.create_access_token(refresh_token_data)
        await self.set_token(token=access_token, token_type=config.auth.access_token_name)
