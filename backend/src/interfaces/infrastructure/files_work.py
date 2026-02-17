from typing import Protocol
from typing import Type, Callable


class IFileStorage(Protocol):
    async def save_file(self, file: Type[Callable], filename: str) -> str | None:
        ...
