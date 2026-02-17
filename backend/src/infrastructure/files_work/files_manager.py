from src.interfaces.infrastructure.files_work import IFileStorage


class FilesManager:
    def __init__(self, file_storage: IFileStorage):
        self.file_storage = file_storage
