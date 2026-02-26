from collections import defaultdict
from fastapi import WebSocket
from typing import Dict, List


class ChatConnectionManager:
    def __init__(self):
        self.connections: Dict[int, List[WebSocket]] = defaultdict(list)

    async def connect(self, chat_id: int, ws: WebSocket):
        await ws.accept()
        self.connections[chat_id].append(ws)

    def disconnect(self, chat_id: int, ws: WebSocket):
        if chat_id in self.connections:
            self.connections[chat_id].remove(ws)
            if not self.connections[chat_id]:
                del self.connections[chat_id]

    async def broadcast(self, chat_id: int, message: dict):
        for ws in self.connections.get(chat_id, []):
            await ws.send_json(message)


manager = ChatConnectionManager()
