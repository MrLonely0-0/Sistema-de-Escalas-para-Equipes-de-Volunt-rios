import api from './client'

export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/token/', { email, password }),
  
  register: (email: string, password: string, firstName: string, lastName: string) =>
    api.post('/users/register/', {
      email,
      password,
      password_confirm: password,
      first_name: firstName,
      last_name: lastName,
    }),
  
  me: () => api.get('/users/me/'),
  
  updateProfile: (data: any) =>
    api.put('/users/me_update/', data),
}

export const teamsAPI = {
  list: () => api.get('/teams/'),
  
  create: (data: any) => api.post('/teams/', data),
  
  detail: (id: string) => api.get(`/teams/${id}/`),
  
  update: (id: string, data: any) => api.put(`/teams/${id}/`, data),
  
  invite: (id: string, userId: string) =>
    api.post(`/teams/${id}/invite/`, { user_id: userId }),
  
  join: (code?: string, token?: string) =>
    api.post('/teams/join/', { code, token }),
  
  getMembers: (id: string) => api.get(`/teams/${id}/members/`),
  
  getRoles: (teamId: string) => api.get(`/teams/${teamId}/roles/`),
  
  createRole: (teamId: string, data: any) =>
    api.post(`/teams/${teamId}/roles/`, data),
  
  getAvailability: (teamId: string) =>
    api.get(`/teams/${teamId}/availability/overview/`),
}

export const schedulesAPI = {
  getAssignments: () => api.get('/schedules/assignments/'),
  
  getUpcoming: () => api.get('/schedules/assignments/upcoming/'),
  
  confirmAssignment: (id: string) =>
    api.post(`/schedules/assignments/${id}/confirm/`, {}),
  
  cancelAssignment: (id: string) =>
    api.post(`/schedules/assignments/${id}/cancel/`, {}),
}

export const notificationsAPI = {
  list: () => api.get('/notifications/'),
  
  unread: () => api.get('/notifications/unread/'),
  
  markAsRead: (id: string) =>
    api.post(`/notifications/${id}/mark_as_read/`, {}),
  
  getPreferences: () =>
    api.get('/notifications/preferences/get_preferences/'),
  
  setPreferences: (data: any) =>
    api.put('/notifications/preferences/set_preferences/', data),
}
