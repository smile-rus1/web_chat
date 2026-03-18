import styles from "./DeleteContactModal.module.css"

interface Props {
  contactId: number
  onConfirm: (contactId: number) => void
  onCancel: () => void
}

export const DeleteContactModal = ({
  contactId,
  onConfirm,
  onCancel
}: Props) => {
  return (
    <div className={styles.overlay}>

      <div className={styles.modal}>
        <h3>Вы действительно хотите удалить этот контакт?</h3>
        <div className={styles.buttons}>

          <button
            className={styles.cancel}
            onClick={onCancel}
          >
            Отмена
          </button>
          <button
            className={styles.confirmDelete}
            onClick={() => onConfirm(contactId)}
          >
            Удалить
          </button>
        </div>
      </div>
    </div>
  )
}