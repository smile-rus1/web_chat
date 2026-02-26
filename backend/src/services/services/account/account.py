import json
import random
import uuid
from abc import ABC

from loguru import logger

from src.dto.db.account.account import Account
from src.dto.services.account.account import CreateAccountDTO, AccountDTO, UpdateAccountDTO
from src.infrastructure.exceptions.account.account import (
    AccountNotFoundByPhone,
    BaseAccountException,
    AccountAlreadyExist,
    AccountAlreadyExistsWithPhone,
    AccountNotFoundByID
)
from src.interfaces.infrastructure.redis_db import IRedisDB
from src.interfaces.services.transaction_manager import IBaseTransactionManager
from src.services.exceptions.acc import (
    AccountAlreadyExistService,
    AccountAlreadyExistsWithPhoneNumberService,
    BaseServiceAccountExceptions,
    InvalidSecretCode, AccountNotFoundByIDService
)


class AccountUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm


class CreateAccount(AccountUseCase):
    async def __call__(
            self,
            token: str,
            account_dto: CreateAccountDTO,
            redis_db: IRedisDB
    ) -> AccountDTO:
        account_data = await redis_db.get(token)
        if account_data is None:
            raise InvalidSecretCode()

        account_data = json.loads(account_data)
        account = Account(
            username=account_dto.username,
            first_name=account_dto.first_name,
            last_name=account_dto.last_name,
            country=account_data.get("country"),
            phone_number=account_data.get("phone_number")
        )

        try:
            account_db = await self._tm.account_repo.create_account(account)
            await self._tm.commit()

            return AccountDTO(
                username=account_db.username,
                first_name=account_db.first_name,
                last_name=account_db.last_name,
                phone_number=account_db.phone_number,
                country=account_db.country,
                email=account_db.email
            )

        except (BaseAccountException, AccountAlreadyExist, AccountAlreadyExistsWithPhone) as exc:
            logger.bind(
                app_name=f"{CreateAccount.__name__}"
            ).error(f"WITH DATA {account}\nMESSAGE: {exc}")
            await self._tm.rollback()
            match exc:
                case (AccountAlreadyExist()):
                    raise AccountAlreadyExistService(account.username)
                case (AccountAlreadyExistsWithPhone()):
                    raise AccountAlreadyExistsWithPhoneNumberService(phone_number=account.phone_number)
                case (BaseAccountException()):
                    raise BaseServiceAccountExceptions()


class RegisterAccount(AccountUseCase):
    async def __call__(
            self,
            phone_number: str,
            country: str,
            redis_db: IRedisDB
    ) -> str:
        try:
            account = await self._tm.account_repo.get_account_by_phone(phone_number)

        except AccountNotFoundByPhone:
            account = None

        if account is not None:
            raise AccountAlreadyExistsWithPhoneNumberService(phone_number)

        secret_code = random.randint(100_000, 999_999)

        await redis_db.set(
            key=str(secret_code),
            value=json.dumps({"phone_number": phone_number, "country": country}),
            expire=300
        )
        # тут будет допустим логика прихода сообщения на телефон
        print({"phone_number": phone_number, "country": country})
        print(secret_code)

        return str(secret_code)


class ConfirmRegister(AccountUseCase):
    async def __call__(self, secret_code: str, redis_db: IRedisDB) -> str:
        account_data = await redis_db.get(secret_code)
        if account_data is None:
            raise InvalidSecretCode()

        account_data = json.loads(await redis_db.get(secret_code))

        token = uuid.uuid4().hex
        await redis_db.set(
            key=token,
            value=json.dumps(
                {"phone_number": account_data.get('phone_number'), "country": account_data.get('country')}
            ),
            expire=600
        )
        return token


class UpdateAccount(AccountUseCase):
    async def __call__(
            self,
            account_dto: UpdateAccountDTO,
    ) -> AccountDTO:
        try:
            old_account = await self._tm.account_repo.get_account_by_id(account_dto.account_id)
        except AccountNotFoundByID:
            raise AccountNotFoundByIDService(account_dto.account_id)

        if account_dto.updating_account_id != old_account.account_id:
            account_dto.updating_account_id = old_account.account_id

        account = Account(
            account_id=account_dto.updating_account_id,
            username=account_dto.username,
            first_name=account_dto.first_name,
            last_name=account_dto.last_name,
            phone_number=account_dto.phone_number,
            country=account_dto.country,
            image_url=account_dto.image_url,
            email=account_dto.email
        )

        try:
            await self._tm.account_repo.update_account(account)
            await self._tm.commit()

        except (BaseAccountException, AccountAlreadyExist, AccountAlreadyExistsWithPhone) as exc:
            logger.bind(
                app_name=f"{UpdateAccount.__name__}"
            ).error(f"WITH DATA {account}\nMESSAGE: {exc}")
            await self._tm.rollback()

            match exc:
                case (AccountAlreadyExist()):
                    raise AccountAlreadyExistService(account.username)
                case (AccountAlreadyExistsWithPhone()):
                    raise AccountAlreadyExistsWithPhoneNumberService(phone_number=account.phone_number)
                case (BaseAccountException()):
                    raise BaseServiceAccountExceptions()

        return AccountDTO(
            username=account_dto.username,
            first_name=account_dto.first_name,
            last_name=account_dto.last_name,
            phone_number=account_dto.phone_number,
            country=account_dto.country,
            email=account_dto.email
        )


class GetAccountByID(AccountUseCase):
    async def __call__(self, account_id: int) -> AccountDTO:
        try:
            account = await self._tm.account_repo.get_account_by_id(account_id)
        except AccountNotFoundByID:
            raise AccountNotFoundByIDService(account_id)

        return AccountDTO(
            username=account.username,
            first_name=account.first_name,
            last_name=account.last_name,
            phone_number=account.phone_number,
            image_url=account.image_url,
            country=account.country,
            email=account.email
        )


class DeleteAccount(AccountUseCase):
    async def __call__(self, current_account_id: int, delete_account_id: int) -> None:
        try:
            account = await self._tm.account_repo.get_account_by_id(delete_account_id)
        except AccountNotFoundByID:
            raise AccountNotFoundByIDService(delete_account_id)

        if current_account_id != account.account_id:
            raise AccountNotFoundByIDService(delete_account_id)

        await self._tm.account_repo.delete_account(delete_account_id)
        await self._tm.commit()


class AccountService:
    def __init__(
            self,
            tm: IBaseTransactionManager,
            redis_db: IRedisDB
    ):
        self._tm = tm
        self._redis_db = redis_db

    async def create_account(self, token: str, account_dto: CreateAccountDTO) -> AccountDTO:
        return await CreateAccount(tm=self._tm)(token, account_dto, self._redis_db)

    async def update_account(self, account_dto: UpdateAccountDTO) -> AccountDTO:
        return await UpdateAccount(tm=self._tm)(account_dto)

    async def get_account_by_id(self, account_id: int) -> AccountDTO:
        return await GetAccountByID(tm=self._tm)(account_id)

    async def delete_account(self, current_account_id: int, delete_account_id: int) -> None:
        return await DeleteAccount(tm=self._tm)(current_account_id, delete_account_id)

    async def register(self, phone_number: str, country: str) -> str:
        return await RegisterAccount(tm=self._tm)(phone_number, country, self._redis_db)

    async def confirm_register(self, secret_code: str) -> str:
        return await ConfirmRegister(tm=self._tm)(secret_code, self._redis_db)
