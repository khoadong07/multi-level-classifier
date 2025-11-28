// Authentication utilities
export interface User {
  username: string
  role: 'admin' | 'user'
  must_change_password: boolean
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export const setAuth = (auth: AuthResponse) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('token', auth.access_token)
    localStorage.setItem('user', JSON.stringify(auth.user))
  }
}

export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token')
  }
  return null
}

export const getUser = (): User | null => {
  if (typeof window !== 'undefined') {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  }
  return null
}

export const clearAuth = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
}

export const isAuthenticated = (): boolean => {
  return !!getToken()
}

export const isAdmin = (): boolean => {
  const user = getUser()
  return user?.role === 'admin'
}
