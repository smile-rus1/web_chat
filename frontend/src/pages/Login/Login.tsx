import { useState, useMemo } from 'react'
import { api } from '../../services/api'
import { useNavigate } from 'react-router-dom'
import styles from './Login.module.css'

type Step = 'phone' | 'confirm'

export const Login = () => {
  const navigate = useNavigate()

  const [step, setStep] = useState<Step>('phone')
  const [phone, setPhone] = useState('')
  const [secretCode, setSecretCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [backendMessage, setBackendMessage] = useState<string | null>(null)
  const [accountNotFound, setAccountNotFound] = useState(false)

  const handlePhoneChange = (value: string) => {
    setPhone(value.replace(/\D/g, ''))
  }

  const handleSecretChange = (value: string) => {
    setSecretCode(value.replace(/\D/g, ''))
  }

  const isValidPhone = useMemo(() => {
    return phone.length >= 7
  }, [phone])

  // 1️⃣ Проверка телефона
  const handleCheckPhone = async () => {
    setError(null)
    setBackendMessage(null)
    setAccountNotFound(false)
    setLoading(true)

    try {
      const response = await api.post('auth/check_account_phone', {
        phone_number: "+" + phone,
      })

      if (response.data.message) {
        setBackendMessage(response.data.message)
        setStep('confirm')
      }
    } catch (err: any) {
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Ошибка проверки телефона'

      if (message.includes('not found')) {
        setAccountNotFound(true)
      }

      setError(message)
    } finally {
      setLoading(false)
    }
  }

  // 2️⃣ Логин по коду
  const handleLogin = async () => {
    setError(null)
    setLoading(true)

    try {
      await api.post('auth/login', {
        secret_code: secretCode,
      })

      navigate('/chat')
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Ошибка авторизации'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h2 className={styles.title}>Вход</h2>

        {error && <div className={styles.errorBox}>{error}</div>}
        {backendMessage && (
          <div className={styles.successBox}>{backendMessage}</div>
        )}

        {step === 'phone' && (
          <>
            <input
              type="tel"
              placeholder="Введите номер телефона"
              value={phone}
              onChange={(e) => handlePhoneChange(e.target.value)}
              className={styles.input}
            />

            <button
              disabled={!isValidPhone || loading}
              onClick={handleCheckPhone}
              className={styles.button}
            >
              {loading ? 'Проверка...' : 'Продолжить'}
            </button>

            {accountNotFound && (
              <button
                className={styles.linkButton}
                onClick={() => navigate('/register')}
              >
                Перейти к регистрации
              </button>
            )}
          </>
        )}

        {step === 'confirm' && (
          <>
            <input
              type="tel"
              placeholder="Введите секретный код"
              value={secretCode}
              onChange={(e) => handleSecretChange(e.target.value)}
              className={styles.input}
            />

            <button
              disabled={secretCode.length < 4 || loading}
              onClick={handleLogin}
              className={styles.button}
            >
              {loading ? 'Авторизация...' : 'Войти'}
            </button>
          </>
        )}
      </div>
    </div>
  )
}
