const ACCESS_TOKEN_KEY = 'access_token'

function getCookie(name: string) {
  const match = document.cookie.match(
    new RegExp('(^| )' + name + '=([^;]+)')
  )
  return match ? match[2] : null
}

export const authService = {
  isAuthenticated() {
    return !!getCookie(ACCESS_TOKEN_KEY)
  },
}