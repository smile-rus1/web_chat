import os
import uuid
from abc import ABC
from typing import Type, Callable

from src.core.config_reader import config
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


class GetImage(FilesWorkUseCase):
    def __call__(self, full_filename: str) -> str | None:
        try:
            # тут конечно же нужно было бы подправить, чтобы название просто подставлялось, а не путь полностью брался
            name_file = full_filename.split("\\")[-1]
            path_to_file = config.files_work.url_storage_location + name_file
            return path_to_file

        except AttributeError:
            return None


class FilesWorkService:
    def __init__(self, files_manager: FilesManager):
        self._fm = files_manager

    async def upload_image(self, file: Type[Callable], filename: str) -> str | None:
        return await UploadImage(self._fm)(file, filename)

    def get_image(self, full_filename: str) -> str | None:
        return GetImage(self._fm)(full_filename)
