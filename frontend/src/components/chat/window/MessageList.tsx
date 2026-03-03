import { useRef, useEffect } from "react"
import type { MouseEvent } from "react"
import styles from "./MessageList.module.css"
import type { ChatMessagesDTO } from "../../../types/chat.types"

interface Props {
  messages: ChatMessagesDTO[]
  currentUserId: number

  msgMenuId: number | null
  setMsgMenuId: (id: number | null) => void

  onStartEdit: (msg: ChatMessagesDTO) => void
  onDeleteRequest: (messageId: number) => void
  setConfirmDeleteMsgId: (id: number | null) => void
}

export const MessageList = ({
  messages,
  currentUserId,
  msgMenuId,
  setMsgMenuId,
  onStartEdit,
  onDeleteRequest,
  setConfirmDeleteMsgId
}: Props) => {

  const menuRef = useRef<HTMLDivElement | null>(null)

  // закрытие меню при клике вне
  useEffect(() => {
    const handleClick = (e: any) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMsgMenuId(null)
      }
    }

    document.addEventListener("click", handleClick)
    return () => document.removeEventListener("click", handleClick)
  }, [])

  return (
    <div className={styles.messages}>

      {messages.map(msg => {

        const isOwner = msg.sender_id === currentUserId

        return (
          <div
            key={msg.message_id}
            className={`
              ${styles.message}
              ${isOwner ? styles.myMessage : styles.otherMessage}
            `}
            onContextMenu={(e: MouseEvent) => {
              if (!isOwner) return
              e.preventDefault()
              setMsgMenuId(msg.message_id)
            }}
            ref={msgMenuId === msg.message_id ? menuRef : null}
          >

            {msg.message_text}

            {msg.updated_at && (
              <div className={styles.editedLabel}>
                изменено {new Date(msg.updated_at).toLocaleTimeString()}
              </div>
            )}

            {isOwner && msgMenuId === msg.message_id && (
              <div className={styles.msgDropdown}>
                <button
                  onClick={() => {
                    onStartEdit(msg)
                    setMsgMenuId(null)
                  }}
                >
                  Изменить
                </button>

                <button
                  onClick={() => {
                    setConfirmDeleteMsgId(msg.message_id)
                    setMsgMenuId(null)
                  }}
                >
                  Удалить
                </button>
              </div>
            )}

          </div>
        )
      })}
    </div>
  )
}