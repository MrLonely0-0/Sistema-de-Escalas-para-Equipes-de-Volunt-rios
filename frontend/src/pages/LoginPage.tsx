import React, { useState } from 'react'
import { Container, Paper, TextField, Button, Box, Typography, Alert } from '@mui/material'
import { useMutation } from '@tanstack/react-query'
import { authAPI } from '../api'
import { useAuthStore } from '../store/auth'
import { useNavigate } from 'react-router-dom'

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const { login } = useAuthStore()
  const navigate = useNavigate()
  
  const loginMutation = useMutation({
    mutationFn: () => authAPI.login(email, password),
    onSuccess: (response: any) => {
      const { access, refresh } = response.data
      login(access, refresh)
      navigate('/dashboard')
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Falha ao fazer login')
    },
  })
  
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError(null)
    loginMutation.mutate()
  }
  
  return (
    <Container maxWidth="sm">
      <Box sx={{ py: 8 }}>
        <Paper sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" sx={{ mb: 3, textAlign: 'center' }}>
            Sistema de Escalas
          </Typography>
          
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="E-mail"
              type="email"
              value={email}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
              margin="normal"
              required
            />
            
            <TextField
              fullWidth
              label="Senha"
              type="password"
              value={password}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
              margin="normal"
              required
            />
            
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              sx={{ mt: 3 }}
              disabled={loginMutation.isPending}
            >
              {loginMutation.isPending ? 'Entrando...' : 'Entrar'}
            </Button>
          </form>
          
          <Typography variant="body2" sx={{ mt: 2, textAlign: 'center' }}>
            Não tem conta? <a href="/register">Registre-se</a>
          </Typography>
        </Paper>
      </Box>
    </Container>
  )
}
