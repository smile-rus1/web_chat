import styles from "./ChatHeader.module.css"
import type { ChatListDTO } from "../../../types/chat.types"

interface Props {
  chat: ChatListDTO
}

export const ChatHeader = ({ chat }: Props) => {

  const participant = chat.participants[0]

  return (
    <div className={styles.chatHeader}>

      {/* Avatar */}
      {participant?.avatar_url && (
        <img
          src={participant.avatar_url}
          alt="avatar"
          className={styles.avatar}
        />
      )}

      {/* Info */}
      <div className={styles.headerInfo}>

        <div className={styles.name}>
          {participant
            ? `${participant.first_name} ${participant.last_name}`
            : `Чат ${chat.chat_id}`}
        </div>

        {participant?.phone_number && (
          <div className={styles.phone}>
            {participant.phone_number}
          </div>
        )}

      </div>

      {/* Three dots menu */}
      <div className={styles.menu}>
        ⋮
      </div>
    </div>
  )
}