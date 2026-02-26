import { useEffect, useState, useRef } from 'react'
import type { MouseEvent } from "react"
import { api } from '../../services/api'
import { ChatSocket } from '../../services/chatSocket'
import styles from './Chat.module.css'
import { authService } from "../../services/auth"

interface ChatParticipantDTO {
  chat_id: number | null
  account_id: number | null
  joined_at?: string | null
}

interface ChatMessagesDTO {
  message_id: number
  chat_id: number
  sender_id: number
  created_at?: string | null
  updated_at?: string | null
  message_text?: string | null
}

interface ChatDTO {
  chat_id: number
  created_at?: string | null
  participants?: ChatParticipantDTO[]
  messages?: ChatMessagesDTO[]
}

export const Chat = () => {
  const [selectedChat, setSelectedChat] = useState<ChatDTO | null>(null)
  const [search, setSearch] = useState('')
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const [chatList, setChatList] = useState<ChatDTO[]>([])
  const [loading, setLoading] = useState(true)

  const [menuOpenId, setMenuOpenId] = useState<number | null>(null)
  const [menuPosition, setMenuPosition] = useState<{ top: number; left: number }>({ top: 0, left: 0 })
  const [confirmDeleteId, setConfirmDeleteId] = useState<number | null>(null)
  const currentUserId = authService.getAccountId()

  const [messages, setMessages] = useState<ChatMessagesDTO[]>([])
  const [messageInput, setMessageInput] = useState('')
  const [msgMenuId, setMsgMenuId] = useState<number | null>(null)
  const [confirmDeleteMsgId, setConfirmDeleteMsgId] = useState<number | null>(null)

  const [editingMessageId, setEditingMessageId] = useState<number | null>(null)
  const [originalMessageText, setOriginalMessageText] = useState<string>("")

  const socketRef = useRef<ChatSocket | null>(null)
  const menuRef = useRef<HTMLDivElement | null>(null)
  const msgMenuRef = useRef<HTMLDivElement | null>(null)

  // ---------------- LOAD CHATS ----------------
  useEffect(() => {
    const loadChats = async () => {
      try {
        const response = await api.get<ChatDTO[]>('/chat/')
        setChatList(response.data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    loadChats()
  }, [])

  // ---------------- CONNECT WS ----------------
  useEffect(() => {
    if (!selectedChat) return

    const socket = new ChatSocket()
    socket.connect(selectedChat.chat_id)
    socketRef.current = socket

    socket.onOpen(() => {
      socket.send({ event: 'get_messages', offset: 0, limit: 50 })
    })

    socket.onMessage((data) => {
      if (data.event === "message_updated") {
        setMessages(prev =>
          prev.map(m =>
            m.message_id === data.message.message_id
              ? data.message
              : m
          )
        )
      }

      if (data.event === 'messages') {
        setMessages(prev => {
          if (prev.length > 0) return prev
          return data.messages
        })
      }

      if (data.event === "new_message") {
          setMessages(prev => {
            if (prev.some(m => m.message_id === data.message.message_id)) {
              return prev
            }
            return [...prev, data.message]
          })
        }

      if (data.event === 'message_deleted') {
        setMessages(prev => prev.filter(m => m.message_id !== data.message_id))
      }
    })

    return () => socket.close()
  }, [selectedChat])

  // ---------------- OUTSIDE CLICK CLOSE ----------------
  useEffect(() => {
    const handleClick = (e: any) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMenuOpenId(null)
      }
      if (msgMenuRef.current && !msgMenuRef.current.contains(e.target)) {
        setMsgMenuId(null)
      }
    }
    document.addEventListener('click', handleClick)
    return () => document.removeEventListener('click', handleClick)
  }, [])

  // ---------------- CHAT DELETE ----------------
  const handleDeleteChat = async (chatId: number) => {
    await api.delete(`/chat/${chatId}`)
    setChatList(prev => prev.filter(c => c.chat_id !== chatId))
    if (selectedChat?.chat_id === chatId) {
      setSelectedChat(null)
      socketRef.current?.close()
    }
    setConfirmDeleteId(null)
  }

  // ---------------- SEND MESSAGE ----------------
  const sendMessage = () => {
  if (!messageInput.trim() || !socketRef.current) return
  if (!selectedChat) return

  // если редактируем
  if (editingMessageId !== null) {
    socketRef.current.send({
      event: 'update_message',
      message_id: editingMessageId,
      chat_id: selectedChat.chat_id,
      new_message_text: messageInput,
      old_message_text: originalMessageText
    })

      setEditingMessageId(null)
      setOriginalMessageText("")
    } else {
      socketRef.current.send({
        event: 'send_message',
        message_text: messageInput
      })
    }

  setMessageInput("")
}

  // ---------------- DELETE MESSAGE ----------------
  const deleteMessage = () => {
    if (!confirmDeleteMsgId || !socketRef.current) return
    socketRef.current.send({ event: 'delete_message', message_id: confirmDeleteMsgId })
    setConfirmDeleteMsgId(null)
  }

  const filteredChats = chatList.filter(chat =>
    `chat ${chat.chat_id}`.toLowerCase().includes(search.toLowerCase())
  )

  if (loading) return <div className={styles.loading}>Загрузка чатов...</div>

  return (
    <div className={styles.layout}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <div className={styles.topBar}>
          <button className={styles.menuButton} onClick={() => setDropdownOpen(!dropdownOpen)}>☰</button>
          {
          dropdownOpen && 
          ( 
          <div className={styles.dropdown}> 
            <div className={styles.dropdownItem}> 
              <a href='/profile' className={styles.dropdownItemLink}>Мой профиль</a> 
            </div> 
            <div className={styles.dropdownItem}> 
              <a href='#' className={styles.dropdownItemLink}>Мои контакты</a>
            </div> 
          </div> 
               )
          }
          <input
            type="text"
            placeholder="Поиск..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className={styles.search}
          />
        </div>

        <div className={styles.chatList}>
          {filteredChats.map(chat => (
            <div
              key={chat.chat_id}
              className={`${styles.chatItem} ${selectedChat?.chat_id === chat.chat_id ? styles.active : ''}`}
              onClick={() => {
                setSelectedChat(chat)
                setMessages([])
              }}
              onContextMenu={(e: MouseEvent) => {
                e.preventDefault()
                setMenuOpenId(chat.chat_id)
                setMenuPosition({ top: e.clientY, left: e.clientX })
              }}
              ref={menuOpenId === chat.chat_id ? menuRef : null}
            >
              Чат {chat.chat_id}

              {menuOpenId === chat.chat_id && (
                <div
                  className={styles.chatDropdown}
                  style={{ top: menuPosition.top, left: menuPosition.left }}
                >
                  <button onClick={() => setConfirmDeleteId(chat.chat_id)}>Удалить чат</button>
                </div>
              )}
            </div>
          ))}
        </div>
      </aside>

      {/* Chat Area */}
      <main className={styles.chatArea}>
        {selectedChat ? (
          <div className={styles.chatContent}>
            <h3>Чат ID: {selectedChat.chat_id}</h3>
            <div className={styles.messages}>
                {messages.map(msg => {
                  const isOwner = msg.sender_id === currentUserId
                return (
                  <div
                    key={msg.message_id}
                    className={`${styles.message}
                    ${isOwner ? styles.myMessage : styles.otherMessage}
                    ${editingMessageId === msg.message_id ? styles.editingMessage : ""}
                  `}
                    onContextMenu={(e: MouseEvent) => {
                      if (!isOwner) return
                      e.preventDefault()
                      setMsgMenuId(msg.message_id)
                    }}
                    ref={msgMenuId === msg.message_id ? msgMenuRef : null}
                  >
                    {msg.message_text}
                    {msg.updated_at && (
                      <div className={styles.editedLabel}>
                        изменено {new Date(msg.updated_at).toLocaleTimeString()}
                      </div>
                    )}

                    {isOwner && msgMenuId === msg.message_id && (
                      <div className={styles.msgDropdown}>
                        <button onClick={() => {
                          setEditingMessageId(msg.message_id)
                          setOriginalMessageText(msg.message_text || "")
                          setMessageInput(msg.message_text || "")
                          setMsgMenuId(null)
                        }}>
                          Изменить
                        </button>
                        <button onClick={() => setConfirmDeleteMsgId(msg.message_id)}>
                          Удалить
                        </button>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>

            <div className={styles.inputArea}>
              {editingMessageId && (
                <button
                  className={styles.cancelEdit}
                  onClick={() => {
                    setEditingMessageId(null)
                    setOriginalMessageText("")
                    setMessageInput("")
                  }}
                >
                  ✕
                </button>
              )}

              <input
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                placeholder={
                  editingMessageId
                    ? "Редактирование сообщения..."
                    : "Введите сообщение..."
                }
              />

              <button onClick={sendMessage}>
                {editingMessageId ? "Сохранить" : "Отправить"}
              </button>
            </div>
          </div>
        ) : (
          <div className={styles.noChat}>Выберите чат</div>
        )}
      </main>

      {/* Confirm chat delete */}
      {confirmDeleteId && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <p>Удалить чат?</p>
            <div className={styles.modalActions}>
              <button onClick={() => handleDeleteChat(confirmDeleteId)}>Да</button>
              <button onClick={() => setConfirmDeleteId(null)}>Отмена</button>
            </div>
          </div>
        </div>
      )}

      {/* Confirm message delete */}
      {confirmDeleteMsgId && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <p>Удалить сообщение?</p>
            <div className={styles.modalActions}>
              <button onClick={deleteMessage}>Да</button>
              <button onClick={() => setConfirmDeleteMsgId(null)}>Отмена</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}