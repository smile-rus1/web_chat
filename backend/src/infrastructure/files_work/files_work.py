import asyncio
from pathlib import Path
from typing import Type, Callable

import aiofiles
from loguru import logger

from src.interfaces.infrastructure.files_work import IFileStorage


class ImageStorage(IFileStorage):
    def __init__(self, base_dir: Path, chunk_size: int = 512 * 1024):
        self.base_dir = base_dir
        self.chunk_size = chunk_size

    async def save_file(self, file: Type[Callable], filename: str) -> str | None:
        path = self.base_dir / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            async with aiofiles.open(path, "wb") as f:
                while chunk := await file.read(self.chunk_size):
                    await f.write(chunk)

        except (OSError, asyncio.CancelledError) as exc:
            if path.exists():
                path.unlink(missing_ok=True)

            logger.bind(
                app_name=f"{ImageStorage.__name__} in {self.save_file.__name__}"
            ).error(f"MESSAGE: {exc}")
            return

        return str(path)
