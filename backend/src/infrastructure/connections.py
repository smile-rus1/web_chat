import redis.asyncio as redis

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from src.infrastructure.db.utils.connection_string_maker import make_connection_string
from src.infrastructure.db_config import DBConfig
from src.infrastructure.redis_db.config import RedisConfig


def get_db_connection(db_config: DBConfig):
    engine = create_async_engine(make_connection_string(db_config))
    maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    return maker


def get_redis_connections(redis_config: RedisConfig):
    pool = redis.ConnectionPool.from_url(
        f"redis://{redis_config.host}:{redis_config.port}/{redis_config.db}",
        max_connections=20,
    )
    return redis.Redis(connection_pool=pool)

