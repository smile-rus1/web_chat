from src.infrastructure.db_config import DBConfig


def make_connection_string(config: DBConfig):
    return (
        f"{config.driver}://{config.user}:{config.password}@{config.host}:{config.port}/{config.db_name}"
    )
