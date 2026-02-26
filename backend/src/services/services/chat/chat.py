import json
from abc import ABC

from loguru import logger

from src.dto.db.chat.chat import Chat, ChatParticipant
from src.dto.services.chat.chat import (
    CreateChatWithUserDTO,
    ChatDTO,
    ChatParticipantDTO
)
from src.infrastructure.exceptions.chat.chat import (
    BaseChatException,
    ChatParticipantNotFound,
    DuplicateChatParticipant, ChatConstraintViolation
)
from src.interfaces.infrastructure.redis_db import IRedisDB
from src.interfaces.services.transaction_manager import IBaseTransactionManager
from src.services.exceptions.chat import (
    BaseServiceChatException,
    ServiceParticipantNotFoundError,
    ServiceDuplicateParticipantError,
    ChatConstraintViolationExceptionService,
)


class ChatUseCase(ABC):
    def __init__(self, tm: IBaseTransactionManager):
        self._tm = tm


class CreateChatWithAccount(ChatUseCase):
    async def __call__(
            self,
            dto: CreateChatWithUserDTO,
            redis_db: IRedisDB
    ) -> ChatDTO:
        chat = Chat(
            participants=[
                ChatParticipant(account_id=account_id) for account_id in dto.participants_ids
            ]
        )
        try:
            chat = await self._tm.chat_repo.create_chat(chat)
            await self._tm.commit()

            for account_id in dto.participants_ids:
                await redis_db.delete(f"chats_{account_id}")

        except BaseChatException as exc:
            logger.bind(
                app_name=f"{CreateChatWithAccount.__name__}"
            ).error(f"WITH DATA {dto}\nMESSAGE: {exc}")
            await self._tm.rollback()

            if isinstance(exc, ChatParticipantNotFound):
                raise ServiceParticipantNotFoundError()

            if isinstance(exc, DuplicateChatParticipant):
                raise ServiceDuplicateParticipantError()

            if isinstance(exc, ChatConstraintViolation):
                raise ChatConstraintViolationExceptionService()

            raise BaseServiceChatException()

        return ChatDTO(
            chat_id=chat.chat_id,
            created_at=chat.created_at,
            participants=[
                ChatParticipantDTO(
                    chat_id=chat.chat_id, account_id=participant.account_id
                )
                for participant in chat.participants
            ],
            messages=None
        )


class DeleteChat(ChatUseCase):
    async def __call__(self, chat_id: int, account_id: int) -> None:
        await self._tm.chat_repo.delete_chat(chat_id, account_id)
        await self._tm.commit()


class GetAllAccountChats(ChatUseCase):

    async def __call__(
        self,
        account_id: int,
        redis_db: IRedisDB
    ) -> list[ChatDTO]:

        key = f"chats_{account_id}"
        cached = await redis_db.get(key)

        if cached is None:
            chats: list[Chat] = await self._tm.chat_repo.get_all_account_chats(account_id)
            serialized = [
                {
                    "chat_id": chat.chat_id,
                    "created_at": chat.created_at.isoformat() if chat.created_at else None,
                    "participants": [
                        {
                            "chat_id": p.chat_id,
                            "account_id": p.account_id,
                        }
                        for p in chat.participants or []
                    ],
                }
                for chat in chats
            ]
            await redis_db.set(key, json.dumps(serialized), expire=300)

        else:
            serialized = json.loads(cached)

        dtos = [
            ChatDTO(
                chat_id=chat["chat_id"],
                created_at=chat["created_at"],
                participants=[
                    ChatParticipantDTO(
                        chat_id=p["chat_id"],
                        account_id=p["account_id"],
                    )
                    for p in chat["participants"]
                ],
                messages=None,
            )
            for chat in serialized
        ]

        return dtos


class ChatService:
    def __init__(
            self,
            tm: IBaseTransactionManager,
            redis_db: IRedisDB
    ):
        self._tm = tm
        self._redis_db = redis_db

    async def create_chat_with_account(self, dto: CreateChatWithUserDTO) -> ChatDTO:
        return await CreateChatWithAccount(self._tm)(dto, self._redis_db)

    async def delete_chat(self, chat_id: int, account_id: int) -> None:
        return await DeleteChat(self._tm)(chat_id, account_id)

    async def get_all_account_chats(self, account_id: int) -> list[ChatDTO]:
        return await GetAllAccountChats(self._tm)(account_id, self._redis_db)
