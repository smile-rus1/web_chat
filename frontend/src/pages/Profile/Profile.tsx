import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../../services/api'
import styles from './Profile.module.css'

interface Account {
  account_id: number
  username: string
  first_name: string
  last_name: string
  phone_number: string
  email: string
  is_admin: boolean
  is_superuser: boolean
  image_url?: string
}

function getCookie(name: string) {
  const match = document.cookie.match(
    new RegExp('(^| )' + name + '=([^;]+)')
  )
  return match ? match[2] : null
}

function parseJwt(token: string) {
  const base64 = token.split('.')[1]
  return JSON.parse(atob(base64))
}

export const Profile = () => {
  const navigate = useNavigate()

  const [account, setAccount] = useState<Account | null>(null)
  const [loading, setLoading] = useState(true)

  const [editMode, setEditMode] = useState(false)
  const [success, setSuccess] = useState(false)
  const [showLogoutModal, setShowLogoutModal] = useState(false)

  const [formData, setFormData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    image: null as File | null,
  })

  useEffect(() => {
    const loadProfile = async () => {
      const token = getCookie('access_token')
      if (!token) {
        navigate('/login')
        return
      }

      const payload = parseJwt(token)
      const accountId = payload.account_id

      try {
        const response = await api.get<Account>(`accounts/${accountId}`)
        setAccount(response.data)

        setFormData({
          phone_number: response.data.phone_number,
          username: response.data.username,
          first_name: response.data.first_name,
          last_name: response.data.last_name,
          image: null,
        })
      } catch {
        navigate('/login')
      } finally {
        setLoading(false)
      }
    }

    loadProfile()
  }, [navigate])

  const handleLogout = async () => {
      try {
        await api.post('/auth/logout') 
      } catch {}

      navigate('/login')
  }

  if (loading) return <div className={styles.loading}>Loading...</div>
  if (!account) return <div className={styles.loading}>Нет данных</div>

  const copy = (value: string) => {
    navigator.clipboard.writeText(value)
  }

  const handleSave = async () => {
    try {
      const token = getCookie('access_token')
      const payload = parseJwt(token!)
      const accountId = payload.account_id

      const data = new FormData()
      data.append('username', formData.username)
      data.append('first_name', formData.first_name)
      data.append('last_name', formData.last_name)
      data.append('phone_number', formData.phone_number)

      if (formData.image) {
        data.append('image', formData.image)
      }
      const response = await api.patch(
        `/accounts/update_account/${accountId}`,
        data
      )

      if (response.status === 202) {
        setAccount(prev =>
          prev
            ? {
                ...prev,
                phone_number: formData.phone_number,
                username: formData.username,
                first_name: formData.first_name,
                last_name: formData.last_name,
              }
            : prev
        )

        setEditMode(false)
        setSuccess(true)

        setTimeout(() => {
          setSuccess(false)
        }, 2500)
      }
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className={styles.container}>
      <button className={styles.back} onClick={() => navigate(-1)}>
        ← Назад
      </button>

      <div className={styles.card}>
        {!editMode && (
          <button
            className={styles.edit}
            onClick={() => setEditMode(true)}
          >
            ✏️
          </button>
        )}

        {success && (
          <div className={styles.success}>
            Данные успешно обновлены
          </div>
        )}

        {!editMode ? (
          <>
            {account.image_url && (
              <img
                src={account.image_url}
                alt="avatar"
                className={styles.avatar}
              />
            )}

            <div className={styles.info}>
              <div className={styles.row}>
                <span>Username:</span>
                <span onClick={() => copy(account.username)}>
                  {account.username}
                </span>
              </div>

              <div className={styles.row}>
                <span>Телефон:</span>
                <span onClick={() => copy(account.phone_number)}>
                  {account.phone_number}
                </span>
              </div>
            </div>
          </>
        ) : (
          <div className={styles.editForm}>
            <input
              type="text"
              value={formData.phone_number}
              onChange={e =>
                setFormData({ ...formData, phone_number: e.target.value })
              }
              placeholder="Phone number"
            />
            <input
              type="text"
              value={formData.username}
              onChange={e =>
                setFormData({ ...formData, username: e.target.value })
              }
              placeholder="Username"
            />

            <input
              type="text"
              value={formData.first_name}
              onChange={e =>
                setFormData({ ...formData, first_name: e.target.value })
              }
              placeholder="First name"
            />

            <input
              type="text"
              value={formData.last_name}
              onChange={e =>
                setFormData({ ...formData, last_name: e.target.value })
              }
              placeholder="Last name"
            />

            <input
              type="file"
              onChange={e =>
                setFormData({
                  ...formData,
                  image: e.target.files?.[0] || null,
                })
              }
            />

            <div className={styles.actions}>
              <button onClick={handleSave}>Сохранить</button>
              <button
                className={styles.cancel}
                onClick={() => setEditMode(false)}
              >
                Отмена
              </button>
            </div>
          </div>
        )}

        <div className={styles.bottomSection}>
  <button className={styles.fullButton}>Язык</button>

  <button
    className={styles.logout}
    onClick={() => setShowLogoutModal(true)}
  >
    Выйти
  </button>
</div>

    {showLogoutModal && (
      <div className={styles.modalOverlay}>
        <div className={styles.modal}>
          <p>Вы действительно хотите выйти?</p>
          <div className={styles.modalActions}>
            <button onClick={handleLogout}>Да</button>
            <button onClick={() => setShowLogoutModal(false)}>
              Отмена
            </button>
          </div>
        </div>
      </div>
    )}
      </div>
    </div>
  )
}
