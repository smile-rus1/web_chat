import axios from 'axios'
import type { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL,
  withCredentials: true,
})

let isRefreshing = false
let failedQueue: {
  resolve: (value?: AxiosResponse<any>) => void
  reject: (error: any) => void
}[] = []

const processQueue = (error: any = null) => {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) {
      reject(error)
    } else {
      resolve()
    }
  })
  failedQueue = []
}

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean }

    // проверка на 401 и что запрос ещё не был повторно отправлен
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // если уже идёт обновление токена, ставим запрос в очередь и ждём
        return new Promise((resolve, reject) => {
          failedQueue.push({
            resolve: () => resolve(api(originalRequest)),
            reject,
          })
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        // запрос на refresh токен
        await api.post('/auth/refresh', {}, { withCredentials: true })

        isRefreshing = false
        processQueue()
        return api(originalRequest)
      } catch (err) {
        isRefreshing = false
        processQueue(err)
        window.location.href = '/login'
        return Promise.reject(err)
      }
    }

    return Promise.reject(error)
  }
)