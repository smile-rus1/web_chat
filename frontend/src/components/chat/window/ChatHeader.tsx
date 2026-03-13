import styles from "./ChatHeader.module.css"
import type { ChatListDTO, ChatListParticipantDTO } from "../../../types/chat.types"

interface Props {
  chat: ChatListDTO
  participant?: ChatListParticipantDTO
  onMenuClick: () => void
}

export const ChatHeader = ({ chat, participant, onMenuClick  }: Props) => {

  return (
    <div className={styles.chatHeader}>
      {/* Avatar */}
      {participant?.avatar_url && (
        <img
          src={participant.avatar_url}
          alt="avatar"
          className={styles.chatHeaderAvatar}
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

      <div 
      className={styles.menu}
      onClick={onMenuClick}
      >
        ⋮
      </div>
    </div>
  )
}