import abc
from typing import Any, Optional


class IRedisDB(abc.ABC):
    @abc.abstractmethod
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, key: str) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def exists(self, key: str) -> bool:
        raise NotImplementedError
