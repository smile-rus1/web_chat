import { jwtDecode } from "jwt-decode"

const ACCESS_TOKEN_KEY = "access_token"

interface AccessTokenPayload {
  account_id: number
  username: string
  first_name: string
  last_name: string
  email: string
  is_admin: boolean
  is_superuser: boolean
  exp: number
  iat: number
}

function getCookie(name: string) {
  const match = document.cookie.match(
    new RegExp("(^| )" + name + "=([^;]+)")
  )
  return match ? match[2] : null
}

export const authService = {
  isAuthenticated(): boolean {
    return !!getCookie(ACCESS_TOKEN_KEY)
  },

  getAccountId(): number | null {
    const token = getCookie(ACCESS_TOKEN_KEY)
    if (!token) return null

    const decoded = jwtDecode<AccessTokenPayload>(token)
    return decoded.account_id
  }
}