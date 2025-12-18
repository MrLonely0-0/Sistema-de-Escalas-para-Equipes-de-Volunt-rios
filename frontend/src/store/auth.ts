import { create } from 'zustand'
import { jwtDecode } from 'jwt-decode'

interface User {
  id: string
  email: string
  firstName: string
  lastName: string
  userType: 'admin' | 'volunteer'
}

interface AuthStore {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (accessToken: string, refreshToken: string) => void
  logout: () => void
  setUser: (user: User) => void
  loadFromStorage: () => void
}

export const useAuthStore = create<AuthStore>((set: any) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: true,
  
  login: (accessToken: string, refreshToken: string) => {
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
    set({
      accessToken,
      refreshToken,
      isAuthenticated: true,
    })
  },
  
  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    set({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
    })
  },
  
  setUser: (user: User) => {
    set({ user })
  },
  
  loadFromStorage: () => {
    const accessToken = localStorage.getItem('access_token')
    const refreshToken = localStorage.getItem('refresh_token')
    
    if (accessToken && refreshToken) {
      try {
        jwtDecode(accessToken)
        set({
          accessToken,
          refreshToken,
          isAuthenticated: true,
          isLoading: false,
        })
      } catch (error) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        set({ isLoading: false })
      }
    } else {
      set({ isLoading: false })
    }
  },
}))
