import styles from "./ChatInput.module.css"

interface Props {
  messageInput: string
  editingMessageId: number | null

  onMessageInputChange: (value: string) => void
  onSendMessage: () => void
  onCancelEdit: () => void
}

export const ChatInput = ({
  messageInput,
  editingMessageId,
  onMessageInputChange,
  onSendMessage,
  onCancelEdit
}: Props) => {

  return (
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
  )
}