import os
import uuid
from abc import ABC
from typing import Type, Callable

from src.infrastructure.files_work.files_manager import FilesManager


class FilesWorkUseCase(ABC):
    def __init__(self, files_manager: FilesManager):
        self._fm = files_manager


class UploadImage(FilesWorkUseCase):
    async def __call__(self, file: Type[Callable], filename: str) -> str | None:
        name, ext = os.path.splitext(filename)
        unique_id = uuid.uuid4().hex
        filename = f"{name}_{unique_id}{ext}"

        path_file = await self._fm.file_storage.save_file(file, filename)

        return path_file


class FilesWorkService:
    def __init__(self, files_manager: FilesManager):
        self._fm = files_manager

    async def upload_image(self, file: Type[Callable], filename: str) -> str | None:
        return await UploadImage(self._fm)(file, filename)

