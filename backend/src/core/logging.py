import os
import sys

from loguru import logger


class BaseLogger:
    def __init__(self, level: str = "INFO"):
        self.level = level


class FileLogger(BaseLogger):
    def __init__(self, logs_dir: str | None = None, level: str = "INFO"):
        super().__init__(level)
        if logs_dir is None:
            logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        logger.add(
            os.path.join(logs_dir, "{time:YYYY.MM.DD}-logs.txt"),
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | NAME SERVICE: {extra[app_name]} | {message}",
            level="INFO",
            rotation="1 day"
        )


class ConsoleLogger(BaseLogger):
    def __init__(self, level: str = "INFO"):
        super().__init__(level)
        logger.add(
            sys.stdout,
            format="<green>{time:HH:mm:ss}</green> | "
                   "<level>{level}</level> | "
                   "<green>NAME SERVICE: {extra[app_name]}</green> | "
                   "{message}",
            level="INFO"
        )


def setup_logging():
    logger.remove()

    FileLogger()
    ConsoleLogger()

