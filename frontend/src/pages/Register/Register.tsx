import { useState, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../../services/api'
import styles from './Register.module.css'

type Country = {
  name: string
  code: string
}

const countries: Country[] = [
    { name: 'Belarus', code: '+375' },
    { name: 'Germany', code: '+49' },
    { name: 'Russia', code: '+7' },
    { name: 'USA', code: '+1' },
]

type Step = 'phone' | 'confirm' | 'create'

export const Register = () => {
  const navigate = useNavigate()

  const [step, setStep] = useState<Step>('phone')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [selectedCountry, setSelectedCountry] = useState(countries[0])
  const [phone, setPhone] = useState('')
  const [secretCode, setSecretCode] = useState('')
  const [token, setToken] = useState('')

  const [username, setUsername] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')

  const handlePhoneChange = (value: string) => {
    setPhone(value.replace(/\D/g, ''))
  }

  const handleSecretChange = (value: string) => {
    setSecretCode(value.replace(/\D/g, ''))
  }

  const isValidPhone = useMemo(() => {
    return phone.length >= 7 && phone.length <= 9
  }, [phone])

  const isValidProfile = useMemo(() => {
    return username.trim() !== '' &&
           firstName.trim() !== '' &&
           lastName.trim() !== ''
  }, [username, firstName, lastName])

  // 1️⃣ Отправка номера
  const handleRegisterPhone = async () => {
    setError(null)
    setLoading(true)

    try {
      const fullPhone = `${selectedCountry.code}${phone}`

      const response = await api.post('accounts/register', {
        phone_number: fullPhone,
        country: selectedCountry.name
      })

      if (response.data.message) {
        setStep('confirm')
      }
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Ошибка регистрации'
      )
    } finally {
      setLoading(false)
    }
  }

  // 2️⃣ Подтверждение кода
  const handleConfirmCode = async () => {
    setError(null)
    setLoading(true)

    try {
      const response = await api.post('accounts/confirm-register', {
        secret_code: secretCode,
      })

      const receivedToken = response.data.register_token
      setToken(receivedToken)
      setStep('create')
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Неверный код'
      )
    } finally {
      setLoading(false)
    }
  }

  // 3️⃣ Создание аккаунта
  const handleCreateAccount = async () => {
    setError(null)
    setLoading(true)

    try {
      await api.post(
        `accounts/create_account/${token}`,
        {
          username: username,
          first_name: firstName,
          last_name: lastName,
        }
      )

      navigate('/login')
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Ошибка создания аккаунта'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h2 className={styles.title}>Регистрация</h2>

        {error && <div className={styles.errorBox}>{error}</div>}

        {step === 'phone' && (
          <>
            <div className={styles.row}>
              <select
                value={selectedCountry.name}
                onChange={(e) =>
                  setSelectedCountry(
                    countries.find(c => c.name === e.target.value)!
                  )
                }
                className={styles.select}
              >
                {countries.map(c => (
                  <option key={c.code}>{c.name}</option>
                ))}
              </select>

              <input
                value={selectedCountry.code}
                disabled
                className={styles.code}
              />
            </div>

            <input
              type="tel"
              placeholder="Введите номер"
              value={phone}
              onChange={(e) => handlePhoneChange(e.target.value)}
              className={styles.input}
            />

            <button
              disabled={!isValidPhone || loading}
              onClick={handleRegisterPhone}
              className={styles.button}
            >
              {loading ? 'Отправка...' : 'Продолжить'}
            </button>
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
              onClick={handleConfirmCode}
              className={styles.button}
            >
              {loading ? 'Проверка...' : 'Подтвердить'}
            </button>
          </>
        )}

        {step === 'create' && (
          <>
            <input
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className={styles.input}
            />

            <input
              placeholder="First name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className={styles.input}
            />

            <input
              placeholder="Last name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className={styles.input}
            />

            <button
              disabled={!isValidProfile || loading}
              onClick={handleCreateAccount}
              className={styles.button}
            >
              {loading ? 'Создание...' : 'Создать аккаунт'}
            </button>
          </>
        )}
      </div>
    </div>
  )
}
