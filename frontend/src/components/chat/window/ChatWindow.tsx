import  { useRef, useEffect, useState } from "react"
import type { MouseEvent } from "react"
import styles from "./ChatWindow.module.css"
import type { ChatListDTO, ChatMessagesDTO } from "../../../types/chat.types"
import { ChatHeader } from "./ChatHeader"
import type { Account } from "../../../types/account.types"

interface Props {
  chat: ChatListDTO | null
  messages: ChatMessagesDTO[]
  currentUserId: number | null
  messageInput: string
  editingMessageId: number | null
  onMessageInputChange: (value: string) => void
  onSendMessage: () => void
  onCancelEdit: () => void
  onStartEdit: (msg: ChatMessagesDTO) => void
  onDeleteMessage: () => void
  onOpenMessageMenu: (id: number) => void
  msgMenuId: number | null
  setMsgMenuId: (id: number | null) => void
  confirmDeleteMsgId: number | null
  setConfirmDeleteMsgId: (id: number | null) => void
  accountPreview: Account | null
  onChatCreated: (account: Account) => void
  onAddContact: (contactId: number) => void
  onEditContact: (contactId: number) => void
  onDeleteChat: (chatId: number) => void
}


export const ChatWindow = ({
  chat,
  messages,
  currentUserId,
  messageInput,
  editingMessageId,
  onMessageInputChange,
  onSendMessage,
  onCancelEdit,
  onStartEdit,
  onOpenMessageMenu,
  msgMenuId,
  setMsgMenuId,
  setConfirmDeleteMsgId,
  accountPreview,
  onChatCreated,
  onAddContact,
  onEditContact,
  onDeleteChat
}: Props) => {

  if (accountPreview) {
    return (
      <main className={styles.chatArea}>

        <div className={styles.previewContainer}>

          {accountPreview.image_url && (
            <img
              src={accountPreview.image_url}
              alt="avatar"
              className={styles.avatarPreview}
            />
          )}

          <div className={styles.previewInfo}>
            <div>
              {accountPreview.first_name} {accountPreview.last_name}
            </div>

            <div>{accountPreview.phone_number}</div>
          </div>

          <button
            className={styles.startChatButton}
            onClick={() => onChatCreated(accountPreview)}
          >
            Начать чат
          </button>
        </div>

      </main>
    )
  }

  
  const dropdownRef = useRef<HTMLDivElement>(null)
  const [headerMenuOpen, setHeaderMenuOpen] = useState(false)
  const headerMenuRef = useRef<HTMLDivElement>(null)
  useEffect(() => {
  if (!dropdownRef.current) return

  const rect = dropdownRef.current.getBoundingClientRect()
  const windowWidth = window.innerWidth

  if (rect.right > windowWidth) {
    dropdownRef.current.style.left = "auto"
    dropdownRef.current.style.right = "100%"
  }

}, [msgMenuId])

useEffect(() => {
  function handleClickOutside(event: globalThis.MouseEvent) {
    if (!dropdownRef.current) return

    if (!dropdownRef.current.contains(event.target as Node)) {
      setMsgMenuId(null)
    }
  }

  document.addEventListener("mousedown", handleClickOutside)

  return () => {
    document.removeEventListener("mousedown", handleClickOutside)
  }
}, [])

useEffect(() => {

  function handleClickOutside(event: globalThis.MouseEvent) {
    if (!headerMenuRef.current) return

    if (!headerMenuRef.current.contains(event.target as Node)) {
      setHeaderMenuOpen(false)
    }
  }

  document.addEventListener("mousedown", handleClickOutside)

  return () => {
    document.removeEventListener("mousedown", handleClickOutside)
  }

}, [])


  if (!chat) {
    return <div className={styles.noChat}>Выберите чат</div>
  }

  return (
    <main className={styles.chatArea}>

      <div className={styles.chatContent}>

        {/* HEADER */}
        <ChatHeader 
          chat={chat} 
          onMenuClick={() => setHeaderMenuOpen(prev => !prev)}
        />
        {headerMenuOpen && (
        <div
          ref={headerMenuRef}
          className={styles.chatHeaderDropdown}
        >

    <button
      className={styles.dropdownItem}
      onClick={() => {
        const participant = chat.participants.find(
          p => p.account_id !== currentUserId
        )

        if (participant) {
          onAddContact(participant.account_id)
        }

        setHeaderMenuOpen(false)
      }}
    >
      Добавить контакт
    </button>

      <button
        className={styles.dropdownItem}
        onClick={() => {
          const participant = chat.participants.find(
            p => p.account_id !== currentUserId
          )

          if (participant) {
            onEditContact(participant.account_id)
          }

          setHeaderMenuOpen(false)
        }}
      >
        Изменить контакт
      </button>

      <button
        className={styles.dropdownItemDelete}
        onClick={() => {
          if (chat) {
            onDeleteChat(chat.chat_id)
          }
        }}
      >
        Удалить чат
      </button>

        </div>
      )}

        {/* MESSAGES */}
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
                  onOpenMessageMenu(msg.message_id)
                }}
              >

                {msg.message_text}

                {msg.updated_at && (
                  <div className={styles.editedLabel}>
                    изменено {new Date(msg.updated_at).toLocaleTimeString()}
                  </div>
                )}

                {isOwner && msgMenuId === msg.message_id && (
                  <div 
                  ref={dropdownRef}
                  className={styles.msgDropdown}
                  >
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

        {/* INPUT */}
        <div className={styles.inputArea}>

          {editingMessageId && (
            <button
              className={styles.cancelEdit}
              onClick={onCancelEdit}
            >
              ✕
            </button>
          )}

          <input
            value={messageInput}
            onChange={(e) => onMessageInputChange(e.target.value)}
            placeholder={
              editingMessageId
                ? "Редактирование сообщения..."
                : "Введите сообщение..."
            }
          />

          <button onClick={onSendMessage}>
            {editingMessageId ? "Сохранить" : "Отправить"}
          </button>
        </div>
      </div>
    </main>
  )
}