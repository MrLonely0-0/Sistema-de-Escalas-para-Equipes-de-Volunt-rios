# 📁 Estrutura do Projeto

```
Sistema-de-Escalas-para-Equipes-de-Voluntários/
│
├── 📂 backend/                          # Django API
│   ├── 📂 app/
│   │   ├── 📂 users/                   # Autenticação, perfil
│   │   │   ├── models.py               # User model
│   │   │   ├── views.py                # API endpoints
│   │   │   ├── serializers.py          # Serialização
│   │   │   └── urls.py
│   │   │
│   │   ├── 📂 teams/                   # Equipes, roles, disponibilidade
│   │   │   ├── models.py               # Team, Role, Availability
│   │   │   ├── views.py                # CRUD endpoints
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   │
│   │   ├── 📂 schedules/               # Escalas, geração, atribuições
│   │   │   ├── models.py               # Schedule, Assignment
│   │   │   ├── views.py                # Geração endpoint
│   │   │   ├── serializers.py
│   │   │   ├── algorithm.py            # Lógica de geração
│   │   │   └── urls.py
│   │   │
│   │   └── 📂 notifications/           # Notificações
│   │       ├── models.py               # Notification
│   │       ├── views.py                # Endpoints
│   │       ├── serializers.py
│   │       ├── service.py              # SendGrid, WhatsApp
│   │       └── urls.py
│   │
│   ├── 📂 config/                      # Configurações Django
│   │   ├── settings.py                 # BD, apps, JWT
│   │   ├── urls.py                     # Rotas principais
│   │   ├── celery.py                   # Celery config
│   │   └── wsgi.py
│   │
│   ├── manage.py                       # Comandos Django
│   ├── requirements.txt                # Dependências pip
│   ├── Dockerfile                      # Imagem Docker
│   └── .env.example
│
├── 📂 frontend/                        # React + TypeScript
│   ├── 📂 src/
│   │   ├── 📂 api/
│   │   │   ├── client.ts               # Axios config
│   │   │   └── index.ts                # Endpoints
│   │   │
│   │   ├── 📂 store/
│   │   │   └── auth.ts                 # Zustand store
│   │   │
│   │   ├── 📂 components/
│   │   │   └── ProtectedRoute.tsx
│   │   │
│   │   ├── 📂 pages/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   └── DashboardPage.tsx
│   │   │
│   │   ├── App.tsx                     # Router
│   │   └── main.tsx                    # Entry point
│   │
│   ├── 📂 public/
│   │   └── index.html
│   │
│   ├── package.json                    # Deps (React, MUI, etc)
│   ├── tsconfig.json                   # TypeScript config
│   ├── vite.config.ts                  # Bundler config
│   ├── .eslintrc.json                  # Linter config
│   ├── Dockerfile                      # Imagem Docker
│   ├── .env.example
│   └── vite-env.d.ts                   # Tipos Vite
│
├── 📄 docker-compose.yml               # Orquestra: Postgres, Redis, Backend, Frontend, Celery
├── 📄 .gitignore
│
├── 📖 README.md                        # Especificação técnica completa
├── 📖 COMECE_AQUI.md                   # 👈 Leia primeiro (visual)
├── 📖 ERRO_MODULOS.txt                 # Por que os erros? (simples)
├── 📖 RESOLUCAO_ERROS.md               # Todas as soluções
├── 📖 SETUP.md                         # Guia detalhado
├── 📖 ERROS_CORRIGIDOS.md              # Auditoria de correções
│
├── 🔧 setup.sh                         # Script setup (Linux/Mac)
├── 🔧 setup.bat                        # Script setup (Windows)
└── 🔧 health-check.sh                  # Verifica dependencies

```

---

## 📊 Fluxo de Dados

```
┌─────────────┐
│  Frontend   │ React + TypeScript + MUI
│  (5173)     │ ↓
└─────┬───────┘
      │ HTTP/JSON
      ↓
┌─────────────────────────────────────┐
│  Backend API (8000)                 │
│  ┌──────────────────────────────────┤
│  │ Django REST Framework + JWT      │
│  │ ├─ users/    (auth, profile)    │
│  │ ├─ teams/    (equipes, roles)   │
│  │ ├─ schedules/(escalas, algo)    │
│  │ └─ notify/   (notificações)     │
│  └──────────────────────────────────┤
│         ↓           ↓           ↓    │
└────┬────────┬───────┬───────────┬────┘
     │        │       │           │
     ↓        ↓       ↓           ↓
┌─────────┐┌──────┐┌──────────┐┌──────────┐
│PostgreSQL││Redis│  Celery   │Celery Beat│
│  (DB)   ││Cache│ (Jobs)    │(Schedule) │
└─────────┘└──────┘└──────────┘└──────────┘
```

---

## 🔄 Ciclo de Vida da Requisição

```
1. Frontend (React)
   └─ user.login(email, password)

2. API Client
   └─ POST /api/auth/token/

3. Backend (Django)
   └─ TokenObtainPairView.post()

4. Resposta
   └─ {access: "...", refresh: "..."}

5. Frontend (Zustand Store)
   └─ localStorage.setItem('access_token', ...)
   └─ Redirect to /dashboard

6. Dashboard
   └─ GET /api/users/me/
   └─ GET /api/teams/
   └─ Render data
```

---

## 📦 Stack Detalhado

| Layer | Tech | Versão | Função |
|-------|------|--------|--------|
| **Frontend** | React | 18.2 | UI |
| | TypeScript | 5.2 | Tipagem |
| | Vite | 5.0 | Bundler |
| | React Router | 6.20 | Routing |
| | Material-UI | 5.14 | Components |
| | React Query | 5.25 | State |
| | Zustand | 4.4 | Store |
| | Axios | 1.6 | HTTP Client |
| | | | |
| **Backend** | Django | 4.2 | Framework |
| | DRF | 3.14 | REST |
| | SimpleJWT | 5.3 | Auth |
| | Celery | 5.3 | Jobs |
| | Redis | 7 | Cache |
| | Postgres | 15 | DB |
| | SendGrid | 6.11 | Email |

---

## 🗄️ Modelos de Dados

```
User
├── id (UUID)
├── email
├── password_hash
├── user_type: 'admin' | 'volunteer'
├── phone
└── created_at

Team
├── id (UUID)
├── name
├── admin_id (FK: User)
├── code (único, convite)
└── members (M2M: TeamMember)

TeamMember
├── user_id (FK)
├── team_id (FK)
├── role: 'admin' | 'volunteer'
└── status: 'pending' | 'active'

Role (Função/Cargo)
├── id (UUID)
├── team_id (FK)
├── name
└── permissions (JSON)

Availability (Disponibilidade)
├── user_id (FK)
├── team_id (FK)
├── day_of_week (0-6)
├── start_time
└── end_time

RegularSchedule (Escala Regular)
├── team_id (FK)
├── day_of_week
├── start_time
├── end_time
├── required_roles: {role_id: qty}
└── frequency: 'weekly' | 'biweekly'

Event (Evento Especial)
├── team_id (FK)
├── title
├── event_date
├── required_roles
└── status: 'draft' | 'published'

GeneratedSchedule (Escala Gerada Mensalmente)
├── team_id (FK)
├── month / year
├── schedule_data (JSON - resultado)
└── status: 'draft' | 'published'

Assignment (Atribuição Individual)
├── generated_schedule_id (FK)
├── user_id (FK)
├── role_id (FK)
├── schedule_date
├── start_time / end_time
└── status: 'assigned' | 'confirmed'

Notification
├── user_id (FK)
├── type: 'assignment' | 'reminder'
├── channel: 'email' | 'whatsapp' | 'push'
├── status: 'pending' | 'sent' | 'failed'
└── scheduled_for / sent_at
```

---

## 🚀 APIs Principais

```
POST   /api/auth/token/              # Login
POST   /api/auth/token/refresh/      # Renovar token

GET    /api/users/me/                # Meu perfil
POST   /api/users/register/          # Registrar

POST   /api/teams/                   # Criar equipe
GET    /api/teams/                   # Listar minhas equipes
POST   /api/teams/{id}/invite/       # Convidar membro
POST   /api/teams/join/              # Entrar em equipe

GET    /api/teams/{id}/roles/        # Roles da equipe
POST   /api/teams/{id}/roles/        # Criar role

GET    /api/availability/            # Minhas disponibilidades
POST   /api/availability/            # Cadastrar disponibilidade

POST   /api/teams/{id}/schedules/generate/  # Gerar escala
GET    /api/teams/{id}/schedules/{month}/{year}/

GET    /api/schedules/assignments/           # Minhas atribuições
GET    /api/schedules/assignments/upcoming/  # Próximas
POST   /api/schedules/assignments/{id}/confirm/
POST   /api/schedules/assignments/{id}/cancel/

GET    /api/notifications/          # Minhas notificações
GET    /api/notification-preferences/
PUT    /api/notification-preferences/
```

---

## 🔐 Autenticação

```
1. Login
   POST /auth/token/
   Body: {email, password}
   Response: {access, refresh}

2. Armazenar
   localStorage.setItem('access_token', access)
   localStorage.setItem('refresh_token', refresh)

3. Usar
   Header: Authorization: Bearer {access_token}

4. Renovar
   POST /auth/token/refresh/
   Body: {refresh}
   Response: {access}

5. Logout
   localStorage.removeItem('access_token')
   localStorage.removeItem('refresh_token')
```

---

## 🎯 Próximas Páginas a Implementar

- [ ] Gestão de Equipes (criar, editar, membros)
- [ ] Configuração de Disponibilidade (calendário)
- [ ] Gerenciamento de Roles
- [ ] Interface de Geração de Escalas
- [ ] Visualização de Escalas
- [ ] Dashboard Admin com Analytics
- [ ] App Mobile (React Native)

---

**Tudo claro? Vá para `COMECE_AQUI.md` para começar! 🚀**
