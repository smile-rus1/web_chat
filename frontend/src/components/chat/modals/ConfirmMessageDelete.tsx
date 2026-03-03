import styles from "./ChatModals.module.css"

interface Props {
  messageId: number
  onConfirm: () => void
  onCancel: () => void
}

export const ConfirmMessageDelete = ({
  messageId,
  onConfirm,
  onCancel
}: Props) => {

  return (
    <div className={styles.overlay}>
      <div className={styles.modal}>

        <p>Удалить сообщение?</p>

        <div className={styles.actions}>
          <button onClick={onConfirm}>
            Да
          </button>

          <button onClick={onCancel}>
            Отмена
          </button>
        </div>

      </div>
    </div>
  )
}