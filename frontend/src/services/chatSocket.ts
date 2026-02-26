export type WSMessage =
  | { event: 'get_messages'; offset: number; limit: number }
  | { event: 'send_message'; message_text: string }
  | { event: 'delete_message'; message_id: number }
  | { 
      event: 'update_message'; 
      message_id: number; chat_id: number; 
      new_message_text: string;
       old_message_text: string
    }



export class ChatSocket {
  private socket: WebSocket | null = null

  connect(chatId: number) {
    this.socket = new WebSocket(
      `${import.meta.env.VITE_WS_URL}/chat/${chatId}`
    )
  }

  onOpen(callback: () => void) {
    if (!this.socket) return
    this.socket.onopen = () => {
      callback()
    }
  }

  onMessage(callback: (data: any) => void) {
    if (!this.socket) return
    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      callback(data)
    }
  }

  send(data: WSMessage) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return
    this.socket.send(JSON.stringify(data))
  }

  close() {
    if (this.socket) {
      this.socket.close()
      this.socket = null
    }
  }
}