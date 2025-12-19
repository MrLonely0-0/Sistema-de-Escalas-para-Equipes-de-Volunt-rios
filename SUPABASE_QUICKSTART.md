# 🚀 Quick Start - Supabase

## 1. Criar Projeto Supabase
- Acesse https://supabase.com
- Login com GitHub
- New Project → `sistema-escalas` → Region: **São Paulo**
- Aguarde 2 minutos

## 2. Copiar Connection String
Settings → Database → Connection string → **Transaction (6543)** → Copy

Exemplo:
```
postgresql://postgres.abc:senha@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

## 3. Configurar Backend

Criar `backend/.env`:
```bash
DATABASE_URL=postgresql://postgres.xxxxx:senha@aws-0-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require
SECRET_KEY=django-insecure-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CELERY_BROKER_URL=redis://redis:6379/0
```

**IMPORTANTE**: Adicione `?sslmode=require` no final!

## 4. Usar o settings correto

**Opção A - Substituir o settings.py atual:**
```bash
cd backend/config
cp settings_supabase.py settings.py
```

**Opção B - Usar DJANGO_SETTINGS_MODULE:**
```bash
# No .env ou docker-compose
DJANGO_SETTINGS_MODULE=config.settings_supabase
```

## 5. Rodar Migrations

```bash
# Docker
docker-compose up -d backend redis celery celery-beat
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# Local
cd backend
python manage.py migrate
python manage.py createsuperuser
```

## 6. GitHub Secrets

No repositório → Settings → Secrets → Actions:
- `DATABASE_URL`: (url do supabase com ?sslmode=require)
- `SECRET_KEY`: (gere com Django)
- `SENDGRID_API_KEY`: (opcional por enquanto)

## 7. Testar

Frontend: http://localhost:5173
Admin: http://localhost:8000/admin

---

**Pronto!** Agora seu Django está usando Supabase PostgreSQL 🎉

Leia `SUPABASE_SETUP.md` para detalhes completos.
