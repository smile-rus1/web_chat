import { useNavigate } from 'react-router-dom'
import styles from './Home.module.css'

export const Home = () => {
  const navigate = useNavigate()

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.logo}>
          WebChat
        </div>

        <div className={styles.buttons}>
          <button
            className={styles.primary}
            onClick={() => navigate('/register')}
          >
            Зарегистрироваться
          </button>

          <button
            className={styles.secondary}
            onClick={() => navigate('/login')}
          >
            Войти
          </button>
        </div>
      </div>
    </div>
  )
}
