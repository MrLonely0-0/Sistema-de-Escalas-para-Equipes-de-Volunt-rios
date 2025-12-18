import axios, { AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios'

const API_URL = (import.meta.env.VITE_API_URL as string) || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    // Axios v1 usa AxiosHeaders; garantir compatibilidade em tempo de tipo
    config.headers = {
      ...(config.headers as any),
      Authorization: `Bearer ${token}`,
    } as any
  }
  return config
})

// Handle token refresh
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = (error.config as InternalAxiosRequestConfig & { _retry?: boolean })
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        })
        
        localStorage.setItem('access_token', response.data.access)
        originalRequest.headers = {
          ...(originalRequest.headers as any),
          Authorization: `Bearer ${response.data.access}`,
        } as any
        return api(originalRequest)
      } catch (refreshError) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
