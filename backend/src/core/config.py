from dataclasses import dataclass

from src.api.auth_config import AuthConfig
from src.api.web_config import WebConfig
from src.infrastructure.db_config import DBConfig
from src.infrastructure.files_work.files_config import FilesWorkConfig
from src.infrastructure.redis_db.config import RedisConfig


@dataclass
class Config:
    web: WebConfig
    db: DBConfig
    redis: RedisConfig
    auth: AuthConfig
    files_work: FilesWorkConfig
