import { useState } from "react"
import styles from "./AddContactModal.module.css"

interface Props {
  contactId: number
  onConfirm: (contactName: string) => void
  onCancel: () => void
}

export const AddContactModal = ({
  contactId,
  onConfirm,
  onCancel
}: Props) => {

  const [contactName, setContactName] = useState("")

  return (
    <div className={styles.overlay}>

      <div className={styles.modal}>

        <h3>Добавить контакт</h3>

        <label className={styles.label}>
          Название контакта
        </label>

        <input
          className={styles.input}
          value={contactName}
          onChange={(e) => setContactName(e.target.value)}
          placeholder="Введите имя контакта"
        />

        <div className={styles.buttons}>

          <button
            className={styles.cancel}
            onClick={onCancel}
          >
            Отмена
          </button>

          <button
            className={styles.confirm}
            onClick={() => onConfirm(contactName)}
            disabled={!contactName.trim()}
          >
            Добавить
          </button>

        </div>

      </div>

    </div>
  )
}