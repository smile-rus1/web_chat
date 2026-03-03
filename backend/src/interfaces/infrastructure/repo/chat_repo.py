from src.dto.db.chat.chat import Chat, Message
from src.dto.db.chat.chat_read import ChatPreview


class IChatRepo:
    async def create_chat(self, chat: Chat) -> Chat:
        ...

    async def delete_chat(self, chat_id: int, account_id: int) -> None:
        ...

    async def is_account_has_permissions_to_chat(self, chat_id: int, account_id: int) -> bool:
        ...

    async def get_messages_from_chat(self, chat_id: int, offset: int, limit: int) -> list[Message]:
        ...

    async def send_message(self, message: Message) -> Message:
        ...

    async def delete_message(self, account_id: int, message_id: int, chat_id: int) -> None:
        ...

    async def get_all_chat_previews(self, account_id: int) -> list[ChatPreview]:
        ...

    async def update_message(self, message: Message) -> Message:
        ...
