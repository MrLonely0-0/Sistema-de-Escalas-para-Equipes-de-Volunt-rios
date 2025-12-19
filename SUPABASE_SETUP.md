# 🗄️ Configuração Supabase - Sistema de Escalas

## Por que Supabase?

✅ **PostgreSQL gerenciado** (compatível 100% com o projeto)  
✅ **Free tier generoso** (500 MB database, 2 GB storage, 50 GB bandwidth)  
✅ **Auth pronta** (OAuth, magic links, JWT) - pode integrar depois  
✅ **Storage** para uploads (fotos de perfil, anexos)  
✅ **Realtime** (subscriptions para notificações ao vivo)  
✅ **Integração com GitHub Actions** (CI/CD fácil)  
✅ **Dashboard visual** (SQL Editor, Table Editor, Auth)  

---

## 🚀 Setup Rápido

### 1. Criar Projeto no Supabase

1. Acesse [supabase.com](https://supabase.com) e faça login com GitHub
2. **New Project**:
   - Name: `sistema-escalas` (ou nome desejado)
   - Database Password: (guarde em local seguro!)
   - Region: **South America (São Paulo)** (menor latência)
   - Pricing Plan: **Free**
3. Aguarde ~2 minutos (criação do projeto)

### 2. Copiar Connection String

No dashboard do Supabase:
1. Vá em **Settings** → **Database**
2. Encontre **Connection string** → **URI**
3. Clique em **Copy** (formato: `postgresql://postgres:[YOUR-PASSWORD]@...`)
4. Exemplo:
   ```
   postgresql://postgres.abcdefghijk:senha123@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
   ```

**Importante**: Use **Transaction mode** (porta 6543) para Django (melhor para connections longas).

### 3. Configurar Localmente

Crie o arquivo `backend/.env`:
```bash
# Supabase Database
DATABASE_URL=postgresql://postgres.xxxxx:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require

# Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Email (SendGrid)
SENDGRID_API_KEY=seu-sendgrid-key
```

**Atenção**: Sempre adicione `?sslmode=require` no final da URL!

### 4. Configurar GitHub Secrets

Para o CI/CD funcionar:

1. No seu repositório GitHub → **Settings** → **Secrets and variables** → **Actions**
2. Clique em **New repository secret**
3. Adicione:

| Name | Value |
|------|-------|
| `DATABASE_URL` | `postgresql://postgres.xxxxx:senha@aws-0...supabase.com:6543/postgres?sslmode=require` |
| `SECRET_KEY` | (gere com `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`) |
| `SENDGRID_API_KEY` | (sua chave SendGrid para emails) |

### 5. Rodar Migrations

**Local (primeira vez):**
```bash
cd /workspaces/Sistema-de-Escalas-para-Equipes-de-Volunt-rios

# Com Docker
docker-compose up -d backend redis celery celery-beat
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# Sem Docker (venv)
cd backend
python manage.py migrate
python manage.py createsuperuser
```

**Automático (GitHub Actions):**
- O workflow já está configurado para rodar migrations em cada deploy

### 6. Verificar Tabelas

No Supabase Dashboard:
1. **Table Editor** → Você verá todas as tabelas criadas pelo Django:
   - `users_user`
   - `teams_team`
   - `schedules_schedule`
   - `notifications_notification`
   - etc.

---

## 🔧 Integração com Django

### settings.py (já configurado)

```python
import environ

env = environ.Env()

DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default='postgresql://localhost/escala_db'
    )
}

# SSL obrigatório para Supabase
DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',
}
```

### docker-compose.yml (atualizado)

O postgres local agora é **opcional**. Se você configurar `DATABASE_URL`, o Django usa o Supabase.

```yaml
services:
  backend:
    environment:
      - DATABASE_URL=${DATABASE_URL}  # Lê do .env ou GitHub Secrets
```

---

## 📊 Recursos Adicionais do Supabase

### 1. Authentication (Opcional - Futuro)

Se quiser substituir JWT do Django por Supabase Auth:
```python
# pip install supabase
from supabase import create_client

supabase = create_client(
    os.environ['SUPABASE_URL'],
    os.environ['SUPABASE_KEY']
)

# Login
user = supabase.auth.sign_in_with_password({
    "email": "user@example.com",
    "password": "senha"
})
```

### 2. Storage (Para fotos de perfil)

```python
# Upload de foto
supabase.storage.from_('avatars').upload(
    f'user_{user_id}.jpg',
    file_data
)

# URL pública
url = supabase.storage.from_('avatars').get_public_url(f'user_{user_id}.jpg')
```

### 3. Realtime (Notificações ao vivo)

No frontend (React):
```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// Escutar novas notificações
supabase
  .channel('notifications')
  .on('postgres_changes', 
    { event: 'INSERT', schema: 'public', table: 'notifications_notification' },
    (payload) => {
      console.log('Nova notificação:', payload.new)
      // Atualizar UI
    }
  )
  .subscribe()
```

---

## 🔐 Segurança

### Row Level Security (RLS)

O Supabase tem RLS (políticas de acesso por linha). Mas como você usa Django ORM, isso não é necessário - o Django já gerencia permissões.

**Recomendação**: Desabilite RLS nas tabelas Django (ou deixe liberado para o usuário `postgres`).

No SQL Editor do Supabase:
```sql
-- Desabilitar RLS em todas as tabelas Django
ALTER TABLE users_user DISABLE ROW LEVEL SECURITY;
ALTER TABLE teams_team DISABLE ROW LEVEL SECURITY;
ALTER TABLE schedules_schedule DISABLE ROW LEVEL SECURITY;
-- etc...
```

---

## 🚀 Deploy Backend (Railway/Render/Vercel)

Após configurar o Supabase, você pode deployar o backend Django em:

### Railway (Recomendado)
```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
cd backend
railway init
railway up
```

No Railway:
- Adicione as variáveis: `DATABASE_URL`, `SECRET_KEY`, `SENDGRID_API_KEY`
- Configure o comando de start: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

### Render
1. Criar Web Service no Render
2. Conectar repositório GitHub
3. Build Command: `cd backend && pip install -r requirements.txt`
4. Start Command: `cd backend && gunicorn config.wsgi:application`
5. Adicionar variáveis de ambiente

---

## 📝 Checklist de Setup

- [ ] Criar projeto no Supabase (região São Paulo)
- [ ] Copiar Connection String (porta 6543, transaction mode)
- [ ] Criar `backend/.env` com `DATABASE_URL`
- [ ] Adicionar `?sslmode=require` no final da URL
- [ ] Rodar `python manage.py migrate`
- [ ] Rodar `python manage.py createsuperuser`
- [ ] Verificar tabelas no Table Editor do Supabase
- [ ] Adicionar secrets no GitHub (`DATABASE_URL`, `SECRET_KEY`)
- [ ] Testar login no frontend local
- [ ] Deploy backend (Railway/Render)
- [ ] Atualizar `VITE_API_URL` no frontend para API deployada

---

## 🆘 Troubleshooting

### Erro: "SSL connection required"
**Solução**: Adicione `?sslmode=require` no `DATABASE_URL`

### Erro: "password authentication failed"
**Solução**: Use a senha correta do projeto (Settings → Database → Reset password se necessário)

### Erro: "too many connections"
**Solução**: Use **Transaction mode** (porta 6543) em vez de Session mode (porta 5432)

### Migrations não rodam
**Solução**: 
```bash
# Verificar conexão
docker-compose exec backend python manage.py dbshell
# Se conectar, rode:
docker-compose exec backend python manage.py migrate --fake-initial
```

---

## 📚 Links Úteis

- [Supabase Dashboard](https://supabase.com/dashboard)
- [Supabase Docs - Django](https://supabase.com/docs/guides/integrations/django)
- [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)
- [Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)

---

**Status: ✅ Configuração completa! Seu Django agora roda com Supabase PostgreSQL.**
