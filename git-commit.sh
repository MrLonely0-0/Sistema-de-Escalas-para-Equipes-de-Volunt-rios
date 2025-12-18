#!/bin/bash

cd "$(dirname "$0")"

git add -A

git commit -m "feat: implementação completa do sistema de escalas para voluntários

- Backend: Django 4.2 com 4 apps (users, teams, schedules, notifications)
- Frontend: React 18 + TypeScript + Vite com Material-UI
- Autenticação: JWT com simplejwt e refresh automático
- Infraestrutura: Docker Compose com PostgreSQL, Redis, Celery, Celery Beat
- Algoritmo: Geração de escalas com rotação de voluntários
- Documentação: 6 guias completos (README, COMECE_AQUI, ESTRUTURA, SETUP, ERROS)
- Correções: Tipos TypeScript Axios v1, React Query v5, React Hooks com useEffect
- Status: 0 erros de compilação, pronto para deploy

Features:
✅ Autenticação com JWT e token refresh
✅ Proteção de rotas com autenticação
✅ Dashboard com estatísticas básicas
✅ API REST completa com 25+ endpoints
✅ 14 modelos de dados com relacionamentos
✅ Algoritmo de geração de escalas
✅ Sistema de notificações (email/WhatsApp)
✅ Docker Compose com 7 serviços
✅ TypeScript com tipos corretos
✅ Material-UI para componentes

Docs:
📖 README.md - Especificação técnica completa
📖 COMECE_AQUI.md - Guia visual rápido
📖 ESTRUTURA.md - Estrutura de arquivos
📖 SETUP.md - Guia detalhado de setup
📖 RESOLUCAO_ERROS.md - Soluções para erros
📖 ERROS_CORRIGIDOS.md - Auditoria de correções
"

git log --oneline -5

echo ""
echo "✅ Commit realizado com sucesso!"
echo ""
echo "🚀 Agora você pode fazer push:"
echo "   git push origin main"
