import json
from abc import ABC
import random

from loguru import logger

from src.infrastructure.exceptions.account.account import AccountNotFoundByPhone
from src.services.exceptions.acc import AccountNotFoundByPhoneService, InvalidSecretCode
from src.interfaces.infrastructure.redis_db import IRedisDB
from src.interfaces.services.transaction_manager import IBaseTransactionManager
from src.interfaces.web.auth import IJWTAuth


class AuthUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm


class CheckAccountPhone(AuthUseCase):
    async def __call__(self, phone_number: str, redis_db: IRedisDB) -> str:
        try:
            account = await self._tm.account_repo.get_account_by_phone(phone_number)

        except AccountNotFoundByPhone:
            logger.bind(
                app_name=f"{AuthenticateAccount.__name__}"
            ).error(f"Account NOT FOUND WITH: {phone_number}")
            raise AccountNotFoundByPhoneService(phone_number=phone_number)

        secret_code = random.randint(100_000, 999_999)
        data_dct = {
            "account_id": account.account_id,
            "username": account.username,
            "phone_number": account.phone_number,
            "email": account.email,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "is_admin": account.is_admin,
            "is_superuser": account.is_superuser,
        }

        await redis_db.set(
            key=str(secret_code),
            value=json.dumps(data_dct),
            expire=300
        )
        # тут будет допустим логика прихода сообщения на телефон
        print(secret_code)

        return str(secret_code)


class AuthenticateAccount(AuthUseCase):
    async def __call__(self, secret_code: str, auth: IJWTAuth, redis_db: IRedisDB) -> dict:
        account_data = await redis_db.get(secret_code)
        if account_data is None:
            raise InvalidSecretCode()

        account_data = json.loads(await redis_db.get(secret_code))

        tokens = await auth.set_tokens(account_data)
        return tokens


class AuthService:
    def __init__(self, tm: IBaseTransactionManager, redis_db: IRedisDB):
        self._tm = tm
        self._redis_db = redis_db

    async def check_account_phone(self, phone_number) -> str:
        return await CheckAccountPhone(self._tm)(phone_number, self._redis_db)

    async def authenticate_account(self, secret_code: str, auth: IJWTAuth) -> dict:
        return await AuthenticateAccount(self._tm)(secret_code, auth, self._redis_db)
