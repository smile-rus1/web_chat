from fastapi import APIRouter, WebSocket, Depends
from loguru import logger
from starlette.websockets import WebSocketDisconnect

from src.api.handlers.handlers.chat.ws_manager import manager
from src.api.handlers.handlers.chat.handlers import handlers
from src.api.permissions import ws_login_required
from src.api.providers.abstract.services import message_service_provider
from src.services.services.chat.message import MessageService


chat_router_ws = APIRouter(
    prefix="/ws/chat",
    tags=["Chat"]
)


@chat_router_ws.websocket("/{chat_id}")
@ws_login_required
async def chat_ws(
        ws: WebSocket,
        chat_id: int,
        message_service: MessageService = Depends(message_service_provider)
):
    await manager.connect(chat_id, ws)
    account = ws.scope["state"]

    has_permission = await message_service.is_account_has_permission_to_chat(
        chat_id,
        account.account_id
    )

    if not has_permission:
        await ws.close(code=1008, reason="Access denied")
        return

    try:
        while True:
            data = await ws.receive_json()
            data["chat_id"] = chat_id

            handler = handlers.get(data["event"])
            res = await handler(data, account, message_service)

            if data["event"] == "get_messages":
                await ws.send_json(res)
            else:
                print(f"BROAD CAST {res}")
                await manager.broadcast(chat_id, res)

    except WebSocketDisconnect:
        manager.disconnect(chat_id, ws)

    except Exception as exc:
        logger.bind(
            app_name="chat_ws"
        ).error(f"EXCEPTION IN WS-CHAT\nMESSAGE: {exc}")
        await ws.close(1011)
