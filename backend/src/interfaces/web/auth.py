import abc
from typing import Any


class IJWTProvider(abc.ABC):
    @abc.abstractmethod
    def _encode_jwt(self, data: dict | Any, expires_delta: int) -> str:
        ...

    @abc.abstractmethod
    def create_access_token(self, data: dict | Any, expires_delta: int | None = None) -> str:
        ...

    @abc.abstractmethod
    def create_refresh_token(self, data: dict | Any, expires_delta: int | None = None) -> str:
        ...

    @abc.abstractmethod
    def decode_token(self, token: str):
        ...

    @abc.abstractmethod
    def read_token(self, token: str) -> dict | None:
        ...


class IJWTAuth(abc.ABC):
    @abc.abstractmethod
    async def set_tokens(self, user: dict) -> dict:
        ...

    @abc.abstractmethod
    async def set_token(self, token: str, token_type: str) -> None:
        ...

    @abc.abstractmethod
    def read_token(self, token_type: str) -> dict | None:
        ...

    @abc.abstractmethod
    async def unset_tokens(self) -> None:
        ...

    async def refresh_access_token(self) -> None:
        ...