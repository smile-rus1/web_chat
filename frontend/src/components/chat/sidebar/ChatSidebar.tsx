import { useState, useRef, useEffect } from "react"
import type { MouseEvent, KeyboardEvent } from "react"
import { api } from "../../../services/api"
import styles from "./ChatSidebar.module.css"
import type { ChatListDTO } from "../../../types/chat.types"
import type { Account } from "../../../types/account.types"
import type { AccountContact } from "../../../types/contact.type"
import { authService } from "../../../services/auth"

interface Props {
  chats: ChatListDTO[]
  selectedChatId: number | null
  search: string
  setSearch: (value: string) => void
  loading: boolean
  onSelectChat: (chat: ChatListDTO) => void
  onDeleteChat: (chatId: number) => void
  onSelectAccount: (account: Account) => void
}

export const ChatSidebar = ({
  chats,
  selectedChatId,
  search,
  setSearch,
  loading,
  onSelectChat,
  onDeleteChat,
  onSelectAccount
}: Props) => {
  const LIMIT = 20

  const [offset, setOffset] = useState(0)
  const [hasMore, setHasMore] = useState(true)
  const listRef = useRef<HTMLDivElement | null>(null)

  const [dropdownOpen, setDropdownOpen] = useState(false)
  const [menuOpenId, setMenuOpenId] = useState<number | null>(null)
  const [menuPosition, setMenuPosition] =
    useState<{ top: number; left: number }>({ top: 0, left: 0 })

  const [showContacts, setShowContacts] = useState(false)
  const [contacts, setContacts] = useState<AccountContact[]>([])
  const [contactsLoading, setContactsLoading] = useState(false)

  const [isSearchingAccounts, setIsSearchingAccounts] = useState(false)
  const [accounts, setAccounts] = useState<Account[]>([])
  const [accountsLoading, setAccountsLoading] = useState(false)

  const menuRef = useRef<HTMLDivElement | null>(null)

  const handleBackToChats = () => {
    setIsSearchingAccounts(false)
    setShowContacts(false)
    setAccounts([])
    setSearch("")
    setOffset(0)
    setHasMore(true)
}
  
const currentAccountId = authService.getAccountId()

const getChatUsername = (chat: ChatListDTO) => {
  const participant = chat.participants.find(
    p => p.account_id !== currentAccountId
  )

  return participant?.username ?? "Unknown"
}

  /* ================= CLOSE CONTEXT MENU ================= */

  useEffect(() => {
    const handleClick = (e: any) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMenuOpenId(null)
      }
    }

    document.addEventListener("click", handleClick)
    return () => document.removeEventListener("click", handleClick)
  }, [])

  /* ================= SEARCH REQUEST ================= */

  const handleSearchAccounts = async (reset = true) => {
  if (!search.trim()) return

  try {
    setAccountsLoading(true)
    setIsSearchingAccounts(true)

    const currentOffset = reset ? 0 : offset

    const response = await api.get<Account[]>("/accounts/", {
      params: {
        username: search,
        phone_number: search,
        offset: currentOffset,
        limit: LIMIT
      }
    })

    const newAccounts = response.data

    if (reset) {
      setAccounts(newAccounts)
      setOffset(LIMIT)
    } else {
      setAccounts(prev => [...prev, ...newAccounts])
      setOffset(prev => prev + LIMIT)
    }

    if (newAccounts.length < LIMIT) {
      setHasMore(false)
    }

  } catch (err) {
    console.error(err)
  } finally {
    setAccountsLoading(false)
  }
}

const loadContacts = async () => {
  try {
    setContactsLoading(true)

    const response = await api.get<AccountContact[]>("/contacts/")

    setContacts(response.data)
    setShowContacts(true)

  } catch (err) {
    console.error(err)
  } finally {
    setContactsLoading(false)
  }
}


  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
  if (e.key === "Enter") {
    setOffset(0)
    setHasMore(true)
    handleSearchAccounts(true)
  }
}

  useEffect(() => {
      if (!isSearchingAccounts) return

      const handleScroll = () => {
        const container = listRef.current
        if (!container || accountsLoading || !hasMore) return

        const { scrollTop, scrollHeight, clientHeight } = container

        if (scrollHeight - scrollTop - clientHeight < 50) {
          handleSearchAccounts(false)
        }
      }

      const container = listRef.current
      container?.addEventListener("scroll", handleScroll)

      return () => {
        container?.removeEventListener("scroll", handleScroll)
      }
    }, [isSearchingAccounts, accountsLoading, hasMore, offset])

  if (loading) {
    return <div className={styles.loading}>Загрузка...</div>
  }

  const filteredChats = chats.filter(chat =>
    chat.participants.some(p =>
      p.username.toLowerCase().includes(search.toLowerCase())
    )
  )

  return (
    <aside className={styles.sidebar}>

      {/* ================= TOP BAR ================= */}

      <div className={styles.topBar}>
        {(isSearchingAccounts || showContacts) && (
            <button
              className={styles.backButton}
              onClick={handleBackToChats}
            >
              ←
            </button>
          )}

          {/* КНОПКА МЕНЮ */}
          {!isSearchingAccounts && !showContacts && (
            <button
              className={styles.menuButton}
              onClick={() => setDropdownOpen(prev => !prev)}
            >
              ☰
            </button>
          )}

        {!isSearchingAccounts && dropdownOpen && (
          <div className={styles.dropdown}>
            <div className={styles.dropdownItem}>
              <a href="/profile">Мой профиль</a>
            </div>
            <div
              className={styles.dropdownItem}
              onClick={() => {
                loadContacts()
                setDropdownOpen(false)
              }}
            >
              Мои контакты
            </div>
          </div>
        )}

        <div className={styles.searchWrapper}>
          <input
            type="text"
            placeholder="Поиск аккаунтов..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={handleKeyDown}
            className={styles.search}
          />

          <button
            className={styles.searchButton}
            onClick={() => {
          setOffset(0)
          setHasMore(true)
          handleSearchAccounts(true)
        }}
          >
            🔍
          </button>
        </div>
      </div>

      {/* ================= LIST ================= */}

      <div 
        className={styles.chatList}
        ref={listRef}
        >
        {isSearchingAccounts ? (
          accountsLoading ? (
            <div className={styles.loading}>Поиск...</div>
          ) : 
          accounts.length === 0 ? (
          <div className={styles.emptyResult}>
            Ничего не было найдено по запросу: <b>{search}</b>
          </div>
        ) :(
            accounts.map(acc => (
              <div
                key={acc.account_id}
                className={styles.chatItem}
                onClick={() => onSelectAccount(acc)}
              >
                <img
                  src={acc.image_url || "/default-avatar.png"}
                  alt={acc.username}
                  className={styles.chatAvatar}
                />

                <div className={styles.chatInfo}>
                  <div className={styles.chatName}>
                    {acc.username}
                  </div>
                </div>
              </div>
            ))
          )
        ): showContacts ? (
          

  /* ================= CONTACTS ================= */

  contactsLoading ? (
    
    <div className={styles.loading}>Загрузка контактов...</div>
  ) : contacts.length === 0 ? (
    <div className={styles.emptyResult}>
      У вас пока нет контактов
    </div>
  ) : (
    
    contacts.map(contact => (
      <div
        key={contact.contact_id}
        className={styles.chatItem}
      >
        <img
          src={contact.image_url || "/default-avatar.png"}
          className={styles.chatAvatar}
        />

        <div className={styles.chatInfo}>
          <div className={styles.chatName}>
            {contact.contact_name}
          </div>

          <div className={styles.chatUsername}>
            @{contact.username}
          </div>
        </div>
      </div>
    ))
  )
) 
        : (
          filteredChats.map(chat => (
            <div
              key={chat.chat_id}
              className={`
                ${styles.chatItem}
                ${selectedChatId === chat.chat_id ? styles.activeItem : ""}
              `}
              onClick={() => onSelectChat(chat)}
              onContextMenu={(e: MouseEvent) => {
                e.preventDefault()
                setMenuOpenId(chat.chat_id)
                setMenuPosition({
                  top: e.clientY,
                  left: e.clientX
                })
              }}
              ref={menuOpenId === chat.chat_id ? menuRef : null}
            >
              <div>
                {getChatUsername(chat)}
              </div>

              {menuOpenId === chat.chat_id && (
                <div
                  className={styles.chatDropdown}
                  style={{
                    top: menuPosition.top,
                    left: menuPosition.left
                  }}
                >
                  <button
                    onClick={() => {
                      onDeleteChat(chat.chat_id)
                      setMenuOpenId(null)
                    }}
                  >
                    Удалить чат
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </aside>
  )
}