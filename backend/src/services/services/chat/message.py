from abc import ABC

from loguru import logger

from src.dto.db.chat.chat import Message
from src.dto.services.chat.chat import SendMessageDTO, MessageDTO, UpdateMessageDTO
from src.infrastructure.exceptions.chat.chat import BaseChatException
from src.interfaces.infrastructure.redis_db import IRedisDB
from src.interfaces.services.transaction_manager import IBaseTransactionManager


class MessageUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm


class GetMessages(MessageUseCase):
    async def __call__(self, chat_id: int, offset: int, limit: int) -> list[MessageDTO]:
        messages = await self._tm.chat_repo.get_messages_from_chat(chat_id, offset, limit)

        return [
            MessageDTO(
                message_id=message.message_id,
                chat_id=chat_id,
                message_text=message.message_text,
                sender_id=message.sender_id,
                created_at=message.created_at,
                updated_at=message.updated_at if message.updated_at != message.created_at else None
            )
            for message in messages
        ]


class IsAccountHasPermissionToChat(MessageUseCase):
    async def __call__(self, chat_id: int, account_id: int) -> bool:
        return await self._tm.chat_repo.is_account_has_permissions_to_chat(chat_id, account_id)


class SendMessage(MessageUseCase):
    async def __call__(self, dto: SendMessageDTO) -> MessageDTO:
        message = Message(
            chat_id=dto.chat_id,
            message_text=dto.message_text,
            sender_id=dto.sender_id
        )
        try:
            res = await self._tm.chat_repo.send_message(message)
            await self._tm.commit()
        except BaseChatException as exc:
            await self._tm.rollback()
            logger.bind(
                app_name=f"{SendMessage.__name__}"
            ).error(f"WITH DATA {message}\nMESSAGE: {exc}")

        return MessageDTO(
            chat_id=res.chat_id,
            sender_id=res.sender_id,
            message_id=res.message_id,
            message_text=res.message_text,
            created_at=res.created_at
        )


class DeleteMessage(MessageUseCase):
    async def __call__(self, account_id: int, message_id: int, chat_id: int) -> None:
        await self._tm.chat_repo.delete_message(account_id, message_id, chat_id)
        await self._tm.commit()


class UpdateMessage(MessageUseCase):
    async def __call__(self, message_dto: UpdateMessageDTO) -> MessageDTO:
        if (
                message_dto.old_message_text == message_dto.new_message_text or
                message_dto.new_message_text == ""
        ):
            return MessageDTO(
                chat_id=message_dto.chat_id,
                sender_id=message_dto.sender_id,
                message_id=message_dto.chat_id,
                message_text=message_dto.new_message_text
            )

        message = Message(
            message_id=message_dto.message_id,
            sender_id=message_dto.sender_id,
            chat_id=message_dto.chat_id,
            message_text=message_dto.new_message_text
        )
        try:
            updated_message = await self._tm.chat_repo.update_message(message)
            await self._tm.commit()

        except BaseChatException as exc:
            await self._tm.rollback()
            logger.bind(
                app_name=f"{SendMessage.__name__}"
            ).error(f"WITH DATA {message}\nMESSAGE: {exc}")

        return MessageDTO(
            chat_id=message_dto.chat_id,
            sender_id=message_dto.sender_id,
            message_id=message_dto.chat_id,
            message_text=updated_message.message_text,
            updated_at=updated_message.updated_at
        )


class MessageService:
    def __init__(
            self,
            tm: IBaseTransactionManager,
            redis_db: IRedisDB
    ):
        self._tm = tm
        self._redis_db = redis_db

    async def is_account_has_permission_to_chat(self, chat_id: int, account_id: int) -> bool:
        return await IsAccountHasPermissionToChat(self._tm)(chat_id, account_id)

    async def get_messages(self, chat_id: int, offset: int, limit: int) -> list[MessageDTO]:
        return await GetMessages(self._tm)(chat_id, offset, limit)

    async def send_message(self, dto: SendMessageDTO) -> MessageDTO:
        return await SendMessage(self._tm)(dto)

    async def delete_message(self, account_id: int, message_id: int, chat_id: int) -> None:
        return await DeleteMessage(self._tm)(account_id, message_id, chat_id)

    async def update_message(self, message_dto: UpdateMessageDTO) -> MessageDTO:
        return await UpdateMessage(self._tm)(message_dto)
