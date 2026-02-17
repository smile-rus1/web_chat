from fastapi import Depends

from src.api.providers.abstract.common import fm_provider, tm_provider, redis_db_provider
from src.infrastructure.files_work.files_manager import FilesManager
from src.interfaces.infrastructure.redis_db import IRedisDB
from src.interfaces.services.transaction_manager import IBaseTransactionManager
from src.services.services.account.account import AccountService
from src.services.services.account.auth import AuthService
from src.services.services.files_work.files_work import FilesWorkService


def account_service_getter(
        tm: IBaseTransactionManager = Depends(tm_provider),
        redis_db: IRedisDB = Depends(redis_db_provider)
):

    return AccountService(tm=tm, redis_db=redis_db)


def auth_service_getter(
        tm: IBaseTransactionManager = Depends(tm_provider),
        redis_db: IRedisDB = Depends(redis_db_provider)
):
    return AuthService(tm=tm, redis_db=redis_db)


def files_work_service_getter(
        fm: FilesManager = Depends(fm_provider)
):
    return FilesWorkService(fm)
