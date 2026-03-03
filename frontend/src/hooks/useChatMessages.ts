import { useState, useCallback, useEffect } from "react"

import type { ChatMessagesDTO } from "../types/chat.types"
import type { UpdateMessage } from "../types/message.types"

interface Params {
  socketRef: React.MutableRefObject<any>
  chatId: number | undefined
}

export const useChatMessages = ({ socketRef, chatId }: Params) => {
  

  const [messages, setMessages] = useState<ChatMessagesDTO[]>([])

    useEffect(() => {
      setMessages([])
    }, [chatId])

  /* ================= SOCKET EVENT HANDLER ================= */

  const handleSocketEvent = useCallback((data: any) => {
    if (!data?.event) return

    if (data.event === "messages") {
      setMessages(data.messages ?? [])
      return
    }

    if (data.event === "new_message") {
      setMessages(prev => {
        if (prev.some(m => m.message_id === data.message.message_id)) {
          return prev
        }
        return [...prev, data.message]
      })
      return
    }

    if (data.event === "message_updated") {
      setMessages(prev =>
        prev.map(m =>
          m.message_id === data.message.message_id
            ? data.message
            : m
        )
      )
      return
    }

    if (data.event === "message_deleted") {
      setMessages(prev =>
        prev.filter(m => m.message_id !== data.message_id)
      )
      return
    }

  }, [])

  /* ================= SEND MESSAGE ================= */

  const sendMessage = useCallback((payload: any) => {
    socketRef.current?.send({
      event: "send_message",
      ...payload
    })
  }, [socketRef])

  /* ================= UPDATE MESSAGE ================= */

  const updateMessage = useCallback((payload: UpdateMessage) => {
    socketRef.current?.send({
      event: "update_message",
      ...payload
    })
  }, [socketRef])

  /* ================= DELETE MESSAGE ================= */

  const deleteMessage = useCallback((messageId: number) => {
    socketRef.current?.send({
      event: "delete_message",
      message_id: messageId
    })
  }, [socketRef])

  return {
    messages,
    setMessages,
    handleSocketEvent,
    sendMessage,
    updateMessage,
    deleteMessage
  }
}