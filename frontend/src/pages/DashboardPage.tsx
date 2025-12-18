import React, { useEffect } from 'react'
import { Container, Box, Typography, Button, Paper, Grid } from '@mui/material'
import { useQuery } from '@tanstack/react-query'
import { authAPI, teamsAPI } from '../api'
import { useAuthStore } from '../store/auth'

export const DashboardPage: React.FC = () => {
  const { user, setUser } = useAuthStore()
  
  const { data: me } = useQuery({
    queryKey: ['user'],
    queryFn: () => authAPI.me(),
  })

  useEffect(() => {
    if (me?.data) {
      setUser(me.data)
    }
  }, [me, setUser])
  
  const { data: teams } = useQuery({
    queryKey: ['teams'],
    queryFn: () => teamsAPI.list(),
  })
  
  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" sx={{ mb: 4 }}>
          Bem-vindo, {user?.firstName || 'Voluntário'}!
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6">Suas Equipes</Typography>
              <Typography variant="h3">{teams?.data?.length || 0}</Typography>
              <Button variant="contained" size="small" sx={{ mt: 2 }}>
                Ver Equipes
              </Button>
            </Paper>
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6">Próximas Escalas</Typography>
              <Typography variant="h3">--</Typography>
              <Button variant="contained" size="small" sx={{ mt: 2 }}>
                Ver Escalas
              </Button>
            </Paper>
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6">Notificações</Typography>
              <Typography variant="h3">--</Typography>
              <Button variant="contained" size="small" sx={{ mt: 2 }}>
                Ver Notificações
              </Button>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  )
}
