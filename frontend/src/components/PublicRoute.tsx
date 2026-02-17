import { Navigate } from 'react-router-dom'
import { authService } from '../services/auth'
import type { ReactNode } from 'react'

export const PublicRoute = ({ children }: { children: ReactNode}) => {
  const isAuth = authService.isAuthenticated()

  if (isAuth) {
    return <Navigate to="/chat" />
  }

  return children
}
