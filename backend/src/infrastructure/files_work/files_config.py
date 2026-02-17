from dataclasses import dataclass


@dataclass
class FilesWorkConfig:
    url_save_file: str
    chunk_size: int
