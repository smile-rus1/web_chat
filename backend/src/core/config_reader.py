import os

from dotenv import load_dotenv

from src.api.auth_config import AuthConfig
from src.core.config import Config
from src.api.web_config import WebConfig
from src.infrastructure.db_config import DBConfig
from src.infrastructure.files_work.files_config import FilesWorkConfig
from src.infrastructure.redis_db.config import RedisConfig


def config_loader() -> Config:
    load_dotenv()

    return Config(
        web=WebConfig(
            port=int(os.getenv("WEB_PORT", 8000)),
            host=os.getenv("WEB_HOST", "localhost"),
            debug=bool(os.getenv("DEBUG")),
            api_v1_str="/api/" + os.getenv("API_VERSION", "v1"),
        ),
        db=DBConfig(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT", 5432)),
            driver=os.getenv("DB_DRIVER"),
            db_name=os.getenv("DB_NAME")
        ),
        redis=RedisConfig(
            host=os.getenv("REDIS_HOST", "127.0.0.1"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0))
        ),
        auth=AuthConfig(
            secret_key=os.getenv("AUTH_SECRET_KEY"),
            algorithm=os.getenv("AUTH_ALGORITHM"),
        ),
        files_work=FilesWorkConfig(
            url_save_file=os.getenv("URL_SAVE_FILE"),
            chunk_size=int(os.getenv("CHUNK_SIZE"))
        )
    )


config = config_loader()
