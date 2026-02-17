import axios from 'axios'


export const api = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL, 
  withCredentials: true, 
})

let isRefreshing = false
let failedQueue: any[] = []

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then(() => api(originalRequest))
          .catch(err => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        // запрос на /refresh
        await api.post('/auth/refresh', {}, { withCredentials: true })

        isRefreshing = false
        processQueue(null, 'refreshed')
        return api(originalRequest)
      } catch (err) {
        isRefreshing = false
        processQueue(err, null)

        window.location.href = '/login'
        return Promise.reject(err)
      }
    }

    return Promise.reject(error)
  }
)
