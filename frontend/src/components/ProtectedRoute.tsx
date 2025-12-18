import React, { useEffect } from 'react'
import { Container, CircularProgress, Box } from '@mui/material'
import { useAuthStore } from '../store/auth'

interface ProtectedRouteProps {
  children: React.ReactNode
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading, loadFromStorage } = useAuthStore()
  
  useEffect(() => {
    loadFromStorage()
  }, [loadFromStorage])
  
  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    )
  }
  
  if (!isAuthenticated) {
    window.location.href = '/login'
    return null
  }
  
  return <>{children}</>
}
