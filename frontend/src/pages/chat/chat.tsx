import { useState } from 'react'
import styles from './Chat.module.css'

type ChatItem = {
  id: number
  name: string
}

const mockChats: ChatItem[] = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
  { id: 3, name: 'Charlie' },
]

export const Chat = () => {
  const [selectedChat, setSelectedChat] = useState<ChatItem | null>(null)
  const [search, setSearch] = useState('')
  const [dropdownOpen, setDropdownOpen] = useState(false)

  const filteredChats = mockChats.filter(chat =>
    chat.name.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className={styles.layout}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <div className={styles.topBar}>
          <div className={styles.dropdownWrapper}>
            <button
              className={styles.menuButton}
              onClick={() => setDropdownOpen(!dropdownOpen)}
            >
              ☰
            </button>

            {dropdownOpen && (
              <div className={styles.dropdown}>
                <div className={styles.dropdownItem}>
                  <a href='/profile' className={styles.dropdownItemLink}>Мой профиль</a>
                  </div>
                <div className={styles.dropdownItem}>
                  <a href='#' className={styles.dropdownItemLink}>Мои контакты</a>
                  </div>
              </div>
            )}
          </div>

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
              key={chat.id}
              className={`${styles.chatItem} ${
                selectedChat?.id === chat.id ? styles.active : ''
              }`}
              onClick={() => setSelectedChat(chat)}
            >
              {chat.name}
            </div>
          ))}
        </div>
      </aside>

      {/* Chat Area */}
      <main className={styles.chatArea}>
        {selectedChat ? (
          <div className={styles.chatContent}>
            <h3>Чат с {selectedChat.name}</h3>
            <div className={styles.placeholder}>
              Сообщения пока не реализованы
            </div>
          </div>
        ) : (
          <div className={styles.noChat}>
            Выберите чат
          </div>
        )}
      </main>
    </div>
  )
}
