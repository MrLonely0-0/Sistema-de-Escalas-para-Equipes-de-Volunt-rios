# Guia de Início Rápido - Sistema de Escalas

## Requisitos

- Docker e Docker Compose
- Git
- Node.js 18+ (para desenvolvimento local do frontend)
- Python 3.11+ (para desenvolvimento local do backend)

## ⚡ Quick Start (Recomendado)

### Opção 1: Com Docker Compose (mais fácil)

```bash
# Entrar no diretório
cd /workspaces/Sistema-de-Escalas-para-Equipes-de-Volunt-rios

# Copiar arquivo de ambiente
cp backend/.env.example backend/.env

# Copiar arquivo de ambiente do frontend
cp frontend/.env.example frontend/.env

# Iniciar tudo
docker-compose up -d

# Criar superusuário em outro terminal
docker-compose exec backend python manage.py createsuperuser
```

### Opção 2: Setup Script

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
cd ..
docker-compose up -d
docker-compose exec backend python manage.py createsuperuser
```

**Windows:**
```bash
setup.bat
cd ..
docker-compose up -d
docker-compose exec backend python manage.py createsuperuser
```

## Configuração com Docker Compose

### 1. Copiar arquivo de ambiente

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 2. Instalar dependências do frontend (se rodar local)

```bash
cd frontend
npm install
cd ..
```

### 3. Iniciar os serviços

```bash
docker-compose up -d
```

Isto iniciará:
- **PostgreSQL**: banco de dados em `localhost:5432`
- **Redis**: cache/fila em `localhost:6379`
- **Backend Django**: API em `http://localhost:8000`
- **Frontend React**: aplicação web em `http://localhost:5173`
- **Celery Worker**: processamento assíncrono
- **Celery Beat**: agendamento de tarefas

### 3. Criar superusuário (admin)

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 4. Acessar a aplicação

- Frontend: http://localhost:5173
- Admin Django: http://localhost:8000/admin
- API: http://localhost:8000/api

## Desenvolvimento Local (sem Docker)

### Backend

```bash
cd backend

# Criar virtual env
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar ambiente
cp .env.example .env

# Migrar banco de dados
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver

# Em outro terminal, iniciar Celery
celery -A config worker --loglevel=info

# Em outro terminal, iniciar Celery Beat
celery -A config beat --loglevel=info
```

### Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar dev server
npm run dev
```

## Estrutura do Projeto

```
├── backend/
│   ├── config/              # Configurações Django
│   ├── app/
│   │   ├── users/           # App de usuários
│   │   ├── teams/           # App de equipes/roles
│   │   ├── schedules/       # App de escalas e geração
│   │   └── notifications/   # App de notificações
│   ├── requirements.txt
│   ├── manage.py
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/             # Chamadas de API
│   │   ├── components/      # Componentes React
│   │   ├── pages/           # Páginas
│   │   ├── store/           # Estado global (Zustand)
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## API Endpoints Principais

### Autenticação
- `POST /api/auth/token/` - Login
- `POST /api/auth/token/refresh/` - Renovar token

### Usuários
- `POST /api/users/register/` - Registrar
- `GET /api/users/me/` - Dados do usuário
- `PUT /api/users/me_update/` - Atualizar perfil
- `GET /api/users/search/?q=termo` - Buscar usuários

### Equipes
- `GET /api/teams/` - Listar equipes
- `POST /api/teams/` - Criar equipe
- `POST /api/teams/join/` - Entrar em equipe (código/token)
- `POST /api/teams/{id}/invite/` - Convidar usuário

### Escalas
- `GET /api/schedules/assignments/` - Minhas atribuições
- `GET /api/schedules/assignments/upcoming/` - Próximas escalas
- `POST /api/schedules/assignments/{id}/confirm/` - Confirmar presença
- `POST /api/schedules/assignments/{id}/cancel/` - Cancelar

### Notificações
- `GET /api/notifications/` - Listar notificações
- `PUT /api/notifications/{id}/mark_as_read/` - Marcar como lida
- `GET /api/notification-preferences/` - Preferências
- `PUT /api/notification-preferences/` - Atualizar preferências

## Variáveis de Ambiente (backend/.env)

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/escala_db

# Redis/Celery
REDIS_URL=redis://localhost:6379/0

# Email (SendGrid)
SENDGRID_API_KEY=your-key
DEFAULT_FROM_EMAIL=noreply@escala.app

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Próximos Passos

1. **Implementar páginas adicionais:**
   - Gestão de equipes (criar, editar, membros)
   - Configuração de disponibilidades
   - Interface de geração de escalas
   - Dashboard de admin

2. **Melhorar algoritmo:**
   - Implementar rodízio avançado
   - Considerar preferências de horário
   - Histórico de 12 semanas

3. **Integração WhatsApp:**
   - Configurar Twilio
   - Criar templates de mensagem
   - Sincronizar com notificações

4. **Monitoramento:**
   - Adicionar logging estruturado
   - Métricas de performance
   - Alertas de erros

5. **Testes:**
   - Testes unitários de algoritmo
   - Testes de integração de API
   - Testes E2E com Cypress/Playwright

## Troubleshooting

### Erro de conexão ao banco
```bash
# Verificar se Postgres está rodando
docker-compose logs postgres

# Resetar banco de dados
docker-compose exec backend python manage.py migrate --fake-initial
```

### Redis/Celery não funciona
```bash
# Verificar logs
docker-compose logs redis
docker-compose logs celery

# Resetar Redis
docker-compose exec redis redis-cli FLUSHALL
```

### CORS errors
Verifique se `CORS_ALLOWED_ORIGINS` contém a URL do frontend.

## Documentação Detalhada

Ver [README.md](README.md) para especificação técnica completa, modelagem de dados, algoritmo, etc.
