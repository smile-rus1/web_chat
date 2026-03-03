from datetime import datetime

from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.dto.db.chat.chat_read import (
    ChatPreview,
    ChatPreviewParticipant
)
from src.infrastructure.exceptions.chat.chat import (
    BaseChatException,
    ChatParticipantNotFound,
    DuplicateChatParticipant,
    ChatConstraintViolation
)
from src.interfaces.infrastructure.repo.chat_repo import IChatRepo
from src.interfaces.infrastructure.sqlalchemy_repo import SqlAlchemyDAO
from sqlalchemy import insert, delete, select, update, asc

from src.dto.db.chat.chat import Chat, Message
from src.infrastructure.db.models import ChatDB, ChatParticipantDB, MessageDB, AccountDB


class ChatRepo(SqlAlchemyDAO, IChatRepo):
    async def create_chat(self, chat: Chat) -> Chat:
        participant_ids = [p.account_id for p in chat.participants]
        participants_key = ":" + ":".join(map(str, sorted(participant_ids))) + ":"
        sql_create_chat = (
            insert(ChatDB)
            .values(
                participants_key=participants_key
            )
            .returning(ChatDB.chat_id, ChatDB.created_at)
        )
        try:
            result = await self._session.execute(sql_create_chat)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{ChatRepo.__name__} in {self.create_chat.__name__}"
            ).error(f"WITH DATA {chat}\nMESSAGE: {exc}")
            raise self._error_parser(exc)

        row = result.one()
        chat_id = row.chat_id
        created_at = row.created_at
        participants: list[ChatParticipantDB] = []

        for participant in chat.participants:
            participants.append(
                ChatParticipantDB(
                    chat_id=chat_id,
                    account_id=participant.account_id
                )
            )

        try:
            self._session.add_all(participants)
            await self._session.flush()

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{ChatRepo.__name__} in {self.create_chat.__name__}"
            ).error(f"WITH DATA {chat}\nMESSAGE: {exc}")
            raise self._error_parser(exc)
        chat.chat_id = chat_id
        chat.created_at = created_at
        return chat

    async def delete_chat(self, chat_id: int, account_id: int) -> None:
        account_id = str(account_id)
        sql = (
            delete(ChatDB)
            .where(
                ChatDB.chat_id == chat_id,
                ChatDB.participants_key.like(f"%:{account_id}:%") |
                ChatDB.participants_key.like(f"{account_id}:%") |
                ChatDB.participants_key.like(f"%:{account_id}") |
                (ChatDB.participants_key == account_id)
            )
        )
        await self._session.execute(sql)

    async def is_account_has_permissions_to_chat(self, chat_id: int, account_id: int) -> bool:
        account_id = str(account_id)
        sql = (
            select(ChatDB.chat_id)
            .where(
                ChatDB.chat_id == chat_id,
                ChatDB.participants_key.like(f"%:{account_id}:%")
            )
        )

        res = (await self._session.execute(sql)).scalar_one_or_none()
        return res is not None

    async def get_messages_from_chat(self, chat_id: int, offset: int, limit: int) -> list[Message]:
        sql = (
            select(MessageDB)
            .where(MessageDB.chat_id == chat_id)
            .offset(offset)
            .limit(limit)
            .order_by(asc(MessageDB.created_at))
        )
        messages = (await self._session.execute(sql)).scalars()
        return [
            Message(
                message_id=message.message_id,
                chat_id=chat_id,
                message_text=message.message_text,
                sender_id=message.sender_id,
                created_at=message.created_at,
                updated_at=message.updated_at
            )
            for message in messages
        ]

    async def send_message(self, message: Message) -> Message:
        sql = (
            insert(MessageDB)
            .values(
                message_text=message.message_text,
                chat_id=message.chat_id,
                sender_id=message.sender_id
            )
            .returning(MessageDB.message_id, MessageDB.created_at, MessageDB.updated_at)
        )
        try:
            result = await self._session.execute(sql)
        except IntegrityError as exc:
            logger.bind(
                app_name=f"{ChatRepo.__name__} in {self.send_message.__name__}"
            ).error(f"WITH DATA {message}\nMESSAGE: {exc}")
            raise self._error_parser(exc)

        row = result.one()
        message_id, created_at, updated_at = row.message_id, row.created_at, row.updated_at

        message.message_id = message_id
        message.created_at = created_at
        message.updated_at = updated_at
        return message

    async def delete_message(self, account_id: int, message_id: int, chat_id: int) -> None:
        sql = (
            delete(MessageDB)
            .where(
                MessageDB.message_id == message_id,
                MessageDB.sender_id == account_id,
                MessageDB.chat_id == chat_id
            )
        )
        await self._session.execute(sql)

    async def get_all_chat_previews(self, account_id: int) -> list[ChatPreview]:
        sql = (
            select(ChatDB)
            .options(selectinload(ChatDB.participants))
            .join(ChatDB.participants)
            .where(AccountDB.account_id == account_id)
        )

        result = await self._session.execute(sql)
        chat_models = result.scalars().unique().all()
        previews = []

        for chat in chat_models:
            participants = [
                ChatPreviewParticipant(
                    account_id=acc.account_id,
                    username=acc.username,
                    avatar_url=acc.image_url,
                    last_name=acc.last_name,
                    first_name=acc.last_name,
                    phone_number=acc.phone_number
                )
                for acc in chat.participants
            ]

            previews.append(
                ChatPreview(
                    chat_id=chat.chat_id,
                    created_at=chat.created_at,
                    participants=participants,
                    last_message=None
                )
            )

        return previews

    async def update_message(self, message: Message) -> Message:
        sql = (
            update(MessageDB)
            .where(
                MessageDB.message_id == message.message_id,
                MessageDB.sender_id == message.sender_id,
                MessageDB.chat_id == message.chat_id
            )
            .values(
                message_text=message.message_text,
                updated_at=datetime.now()
            )
            .returning(MessageDB.updated_at, MessageDB.message_text)
        )
        try:
            result = await self._session.execute(sql)

        except IntegrityError as exc:
            logger.bind(
                app_name=f"{ChatRepo.__name__} in {self.update_message.__name__}"
            ).error(f"WITH DATA {message}\nMESSAGE: {exc}")
            raise self._error_parser(exc)

        row = result.one()
        date, message_text = row.updated_at, row.message_text
        message.updated_at = date
        message.message_text = message_text
        return message

    @staticmethod
    def _error_parser(
            exc: IntegrityError
    ) -> BaseChatException:
        error_message = str(exc).lower()

        if "foreign key" in error_message and "account" in error_message:
            return ChatParticipantNotFound()

        if "duplicate key" in error_message or "unique constraint" in error_message:
            if "chat_participants" in error_message or "hats_participants_key_key" in error_message:
                return DuplicateChatParticipant()
        if "not null" in error_message:
            return ChatConstraintViolation()

        return BaseChatException()
