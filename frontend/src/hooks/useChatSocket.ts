import { useEffect, useRef } from "react"
import { ChatSocket } from "../services/chatSocket"

interface Params {
  chatId: number | undefined
}

export const useChatSocket = ({ chatId }: Params) => {

  const socketRef = useRef<ChatSocket | null>(null)

  useEffect(() => {

    if (!chatId) return

    const socket = new ChatSocket()
    socket.connect(chatId)

    socket.onOpen(() => {  // вот тут просто что-то сделать с этим чтобы допустим у меня шел запрос именно при нажатии на чат, а тут при открытии не делался
      socket.send({
        event: "get_messages",
        offset: 0,
        limit: 50
      })
    })

    socketRef.current = socket

    return () => {
      socket.close()
      socketRef.current = null
    }

  }, [chatId])

  return socketRef
}