import styles from "./ChatModals.module.css"

interface Props {
  onConfirm: () => void
  onCancel: () => void
}

export const ConfirmChatDelete = ({
  onConfirm,
  onCancel
}: Props) => {

  return (
    <div className={styles.overlay}>
      <div className={styles.modal}>

        <p>Удалить чат?</p>

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