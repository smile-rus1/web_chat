from fastapi import APIRouter, status, Depends

from src.api.permissions import login_required
from src.api.providers.abstract.services import chat_service_provider, files_work_service_provider
from src.api.providers.auth import TokenAuthDep
from src.dto.services.chat.chat import CreateChatWithUserDTO
from src.services.services.chat.chat import ChatService
from src.services.services.files_work.files_work import FilesWorkService


chat_router = APIRouter(prefix="/chat", tags=["Chat"])


@chat_router.post(
    "/{account_id}",
    status_code=status.HTTP_201_CREATED
)
@login_required
async def create_chat(
        account_id: int,
        auth: TokenAuthDep,
        chat_service: ChatService = Depends(chat_service_provider)
):
    chat_dto = CreateChatWithUserDTO([account_id, auth.request.state.user.account_id])
    created_chat = await chat_service.create_chat_with_account(chat_dto)

    return created_chat


@chat_router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@login_required
async def delete_chat(
        chat_id: int,
        auth: TokenAuthDep,
        chat_service: ChatService = Depends(chat_service_provider)
):
    await chat_service.delete_chat(chat_id=chat_id, account_id=auth.request.state.user.account_id)


@chat_router.get(
    "/",
    status_code=status.HTTP_200_OK
)
@login_required
async def get_all_preview_chats(
        auth: TokenAuthDep,
        chat_service: ChatService = Depends(chat_service_provider),
        files_work: FilesWorkService = Depends(files_work_service_provider)
):
    chats = await chat_service.get_all_preview_chats(auth.request.state.user.account_id)
    for chat in chats:  # тоже не оптимальный вариант, но пока что пускай так
        for participant in chat.participants:
            participant.avatar_url = files_work.get_image(participant.avatar_url)
    return chats
