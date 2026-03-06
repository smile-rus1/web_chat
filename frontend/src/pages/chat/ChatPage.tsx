import { useState, useEffect} from "react"
import toast from "react-hot-toast"
import { api } from "../../services/api"
import { authService } from "../../services/auth"

import styles from "./Chat.module.css"
import { ChatSidebar } from "../../components/chat/sidebar/ChatSidebar"
import { ChatWindow } from "../../components/chat/window/ChatWindow"
import { ConfirmChatDelete } from "../../components/chat/modals/ConfirmChatDelete"
import { ConfirmMessageDelete } from "../../components/chat/modals/ConfirmMessageDelete"

import { AddContactModal } from "../../components/chat/modals/AddContactModal"
import { EditContactModal } from "../../components/chat/modals/EditContactmodal"

import { useChatSocket } from "../../hooks/useChatSocket"
import { useChatMessages } from "../../hooks/useChatMessages"

import type { ChatListDTO, ChatMessagesDTO } from "../../types/chat.types"
import type { Account } from "../../types/account.types"

export const ChatPage = () => {

  /* ================= AUTH ================= */

  const currentUserId = authService.getAccountId()

  /* ================= CHAT LIST ================= */

  const [chatList, setChatList] = useState<ChatListDTO[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedChat, setSelectedChat] = useState<ChatListDTO | null>(null)
  const [selectedAccountPreview, setSelectedAccountPreview] = useState<Account | null>(null)
  const [search, setSearch] = useState("")
  const [messageInput, setMessageInput] = useState("")
  const [editingMessageId, setEditingMessageId] = useState<number | null>(null)
  const [oldMessageText, setOldMessageText] = useState("")
  const [msgMenuId, setMsgMenuId] = useState<number | null>(null)

  /* ================= MODALS ================= */

  const [confirmDeleteId, setConfirmDeleteId] = useState<number | null>(null)
  const [confirmDeleteMsgId, setConfirmDeleteMsgId] = useState<number | null>(null)
  const [addContactId, setAddContactId] = useState<number | null>(null)
  const [editContactId, setEditContactId] = useState<number | null>(null)

/* ================= HANDLERS ================= */
  const handleOpenMessageMenu = (id: number) => {
    setMsgMenuId(prev => (prev === id ? null : id))
  }
    const handleStartEdit = (msg: ChatMessagesDTO) => {
      setEditingMessageId(msg.message_id)
      setOldMessageText(msg.message_text ?? "")
      setMessageInput(msg.message_text ?? "")
      setMsgMenuId(null)
    }
  const handleCancelEdit = () => {
      setEditingMessageId(null)
      setMessageInput("")
    }
  const handleStartChatFromPreview = async (account: Account) => {

  const existingChat = chatList.find(chat =>
    chat.participants.some(
      p => p.account_id === account.account_id
    )
  )

    if (existingChat) {
      setSelectedChat(existingChat)
      setSelectedAccountPreview(null)
      return
    }

    try {
      const response = await api.post<ChatListDTO>(
        `/chat/${account.account_id}`
      )

      const newChat = response.data
      console.log(newChat)

      setChatList(prev => [...prev, newChat])
      setSelectedChat(newChat)

    } catch (err) {
      console.error("Ошибка создания чата", err)  
    }
      setSelectedAccountPreview(null)
    }

    const handleAddContact = async (contactName: string) => {
      if (!addContactId) return
      try {

        const response = await api.post("/contacts/", {
          contact_id: addContactId,
          contact_name: contactName
        })

        toast.success("Контакт успешно добавлен")

      } catch (err: any) {
        const message = err.response?.data
          if (message.includes("already added")) {
            toast.error("Этот контакт уже добавлен")
          }
          else if (message.includes("cannot add")) {
            toast.error("Вы не можете добавить этот аккаунт")
          }
          else if (message.includes("not found")) {
            toast.error("Пользователь не найден")
          }
          else {
            toast.error("Что-то пошло не так, попробуйте позже")
          }

      }
      setAddContactId(null)
    }

    const handleEditContact = async (contactName: string) => {
      if (!editContactId) return
      try {

        const response = await api.patch("/contacts/update_contact_name", {
          contact_id: editContactId,
          contact_name: contactName
        })

        toast.success("Контакт успешно изменен")

      } catch (err: any) {
        const message = err.response?.data
          if (message.includes("already added")) {
            toast.error("Этот контакт уже добавлен")
          }
          else if (message.includes("cannot add")) {
            toast.error("Вы не можете добавить этот аккаунт")
          }
          else if (message.includes("not found")) {
            toast.error("Пользователь не найден")
          }
          else {
            toast.error("Что-то пошло не так, попробуйте позже")
          }

      }
      setEditContactId(null)
    }

    /* ================= SOCKET ================= */
    const socketRef = useChatSocket({
      chatId: selectedChat?.chat_id
    })


    /* ================= MESSAGES ================= */

    const {
        messages,
        handleSocketEvent,
        sendMessage,
        updateMessage,
        deleteMessage
      } = useChatMessages({
        socketRef,
        chatId: selectedChat?.chat_id
      })
    
    useEffect(() => {
      const socket = socketRef.current
      if (!socket) return

      socket.onMessage(handleSocketEvent)

    }, [socketRef.current, handleSocketEvent])

  /* ================= LOAD CHATS ================= */

  const loadChats = async () => {
    try {
      const response = await api.get<ChatListDTO[]>("/chat/")
      setChatList(response.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadChats()
  }, [])

  /* ================= CHAT DELETE ================= */

  const handleDeleteChat = async (chatId: number) => {
    await api.delete(`/chat/${chatId}`)

    setChatList(prev =>
      prev.filter(chat => chat.chat_id !== chatId)
    )

    if (selectedChat?.chat_id === chatId) {
      setSelectedChat(null)
    }

    setConfirmDeleteId(null)
  }

  /* ================= MESSAGE HANDLERS ================= */

    const handleSendMessage = () => {
      if (!messageInput.trim()) return

        if (editingMessageId) {
          updateMessage({
              message_id: editingMessageId,
              old_message_text: oldMessageText,
              new_message_text: messageInput
            })

            setEditingMessageId(null)
        } else {
          console.log(messageInput)
          sendMessage({
            message_text: messageInput
          })
        }

        setMessageInput("")
      }

  /* ================= RENDER ================= */

  return (
    <div className={styles.layout}>

      {/* ================= SIDEBAR ================= */}

      <ChatSidebar
        chats={chatList}
        selectedChatId={selectedChat?.chat_id ?? null}
        loading={loading}
        search={search}
        setSearch={setSearch}
        onSelectChat={(chat) => {
          setSelectedAccountPreview(null)
          setSelectedChat(chat)
        }}
        onSelectAccount={(account) => {
          setSelectedChat(null)
          setSelectedAccountPreview(account)
        }}
        onDeleteChat={(chatId) => setConfirmDeleteId(chatId)}
      />

      {/* ================= CHAT WINDOW ================= */}

      <ChatWindow
        chat={selectedChat}
        messages={messages}
        currentUserId={currentUserId}

        messageInput={messageInput}
        editingMessageId={editingMessageId}
        onMessageInputChange={setMessageInput}

        onSendMessage={handleSendMessage}
        onCancelEdit={handleCancelEdit}
        onStartEdit={handleStartEdit}
        onDeleteMessage={() => {}}

        onOpenMessageMenu={handleOpenMessageMenu}
        msgMenuId={msgMenuId}
        setMsgMenuId={setMsgMenuId}
        confirmDeleteMsgId={confirmDeleteMsgId}
        setConfirmDeleteMsgId={setConfirmDeleteMsgId}

        accountPreview={selectedAccountPreview}
        onChatCreated={handleStartChatFromPreview}

        onAddContact={(id) => setAddContactId(id)}
        onEditContact={(id) => setEditContactId(id)}
        onDeleteChat={(chatId) => setConfirmDeleteId(chatId)}
      />

      {/* ================= MODALS ================= */}

      {confirmDeleteId && (
        <ConfirmChatDelete
          chatId={confirmDeleteId}
          onConfirm={() => handleDeleteChat(confirmDeleteId)}
          onCancel={() => setConfirmDeleteId(null)}
        />
      )}

      {confirmDeleteMsgId && (
        <ConfirmMessageDelete
          messageId={confirmDeleteMsgId}
          onConfirm={() => deleteMessage(confirmDeleteMsgId)}
          onCancel={() => setConfirmDeleteMsgId(null)}
        />
      )}

      {addContactId && (
        <AddContactModal
          contactId={addContactId}
          onConfirm={handleAddContact}
          onCancel={() => setAddContactId(null)}
        />
      )}
      {editContactId && (
        <EditContactModal
          contactId={editContactId}
          onConfirm={handleEditContact}
          onCancel={() => setEditContactId(null)}
        />
      )}

    </div>
  )
}