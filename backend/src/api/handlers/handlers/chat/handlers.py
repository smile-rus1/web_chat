from src.api.handlers.handlers.chat.response.messages import (
    MessagesEventResponse,
    MessageResponse,
    SendMessageResponse,
    DeleteMessageResponse,
    UpdateMessageResponse
)
from src.dto.services.chat.chat import SendMessageDTO, UpdateMessageDTO
from src.dto.web.auth import ActiveUser
from src.services.services.chat.message import MessageService


async def get_messages(
        data: dict,
        account: ActiveUser,
        message_service: MessageService
):
    messages = await message_service.get_messages(
        chat_id=data.get("chat_id"),
        offset=data.get("offset"),
        limit=data.get("limit")
    )
    response = MessagesEventResponse(
        messages=[MessageResponse.model_validate(m) for m in messages]
    )

    return response.model_dump(mode="json")


async def send_message(
        data: dict,
        account: ActiveUser,
        message_service: MessageService
):
    dto = SendMessageDTO(
        chat_id=data.get("chat_id"),
        message_text=data.get("message_text"),
        sender_id=account.account_id
    )
    res = await message_service.send_message(dto)
    response = SendMessageResponse(
        message=MessageResponse.model_validate(res)
    )

    return response.model_dump(mode="json")


async def delete_message(
        data: dict,
        account: ActiveUser,
        message_service: MessageService
):
    await message_service.delete_message(
        account_id=account.account_id,
        message_id=data.get("message_id"),
        chat_id=data.get("chat_id")
    )
    model = DeleteMessageResponse(message_id=data.get("message_id"))
    return model.model_dump(mode="json")


async def update_message(
        data: dict,
        account: ActiveUser,
        message_service: MessageService
):
    message_dto = UpdateMessageDTO(
        message_id=data.get("message_id"),
        chat_id=data.get("chat_id"),
        sender_id=account.account_id,
        new_message_text=data.get("new_message_text"),
        old_message_text=data.get("old_message_text")
    )

    res = await message_service.update_message(message_dto)
    model = UpdateMessageResponse(
        message=MessageResponse.model_validate(res)
    )
    return model.model_dump(mode="json")


handlers = {
    "get_messages": get_messages,
    "send_message": send_message,
    "delete_message": delete_message,
    "update_message": update_message
}
