import { Navigate } from 'react-router-dom'
import { authService } from '../services/auth'

type Props = {
  children: React.ReactNode
}

export const ProtectedRoute = ({ children }: Props) => {
  if (!authService.isAuthenticated()) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}
