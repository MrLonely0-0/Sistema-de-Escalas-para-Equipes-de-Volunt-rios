import React, { useState } from 'react'
import { Container, Paper, TextField, Button, Box, Typography, Alert } from '@mui/material'
import { useMutation } from '@tanstack/react-query'
import { authAPI } from '../api'
import { useAuthStore } from '../store/auth'
import { useNavigate } from 'react-router-dom'

export const RegisterPage: React.FC = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [error, setError] = useState<string | null>(null)
  const { login } = useAuthStore()
  const navigate = useNavigate()
  
  const registerMutation = useMutation({
    mutationFn: () => authAPI.register(email, password, firstName, lastName),
    onSuccess: () => {
      // Automatically login after registration
      const loginMutation = useMutation({
        mutationFn: () => authAPI.login(email, password),
        onSuccess: (loginResponse: any) => {
          const { access, refresh } = loginResponse.data
          login(access, refresh)
          navigate('/dashboard')
        },
      })
      loginMutation.mutate()
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Falha ao registrar')
    },
  })
  
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError(null)
    registerMutation.mutate()
  }
  
  return (
    <Container maxWidth="sm">
      <Box sx={{ py: 8 }}>
        <Paper sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" sx={{ mb: 3, textAlign: 'center' }}>
            Registrar-se
          </Typography>
          
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Primeiro Nome"
              value={firstName}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFirstName(e.target.value)}
              margin="normal"
              required
            />
            
            <TextField
              fullWidth
              label="Último Nome"
              value={lastName}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setLastName(e.target.value)}
              margin="normal"
              required
            />
            
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
              disabled={registerMutation.isPending}
            >
              {registerMutation.isPending ? 'Registrando...' : 'Registrar'}
            </Button>
          </form>
          
          <Typography variant="body2" sx={{ mt: 2, textAlign: 'center' }}>
            Já tem conta? <a href="/login">Faça login</a>
          </Typography>
        </Paper>
      </Box>
    </Container>
  )
}
