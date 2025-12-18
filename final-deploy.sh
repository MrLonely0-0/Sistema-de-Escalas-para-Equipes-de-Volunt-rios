#!/bin/bash

# Script final de preparação para commit e push

echo "════════════════════════════════════════════════════════════════"
echo "  Sistema de Escalas para Equipes de Voluntários - Deploy"
echo "════════════════════════════════════════════════════════════════"
echo ""

cd "$(dirname "$0")"

# 1. Verifica git
echo "🔍 Verificando git..."
if ! command -v git &> /dev/null; then
    echo "❌ Git não está instalado"
    exit 1
fi
echo "✅ Git ok"

# 2. Status do repositório
echo ""
echo "📋 Status do repositório:"
git status --short | head -20
echo ""

# 3. Opções
echo "════════════════════════════════════════════════════════════════"
echo "  Opções:"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "1️⃣  Fazer commit com tudo"
echo "2️⃣  Ver diferenças (git diff)"
echo "3️⃣  Ver histórico (git log)"
echo "4️⃣  Fazer commit customizado"
echo "5️⃣  Apenas adicionar arquivos (git add -A)"
echo ""
read -p "Escolha uma opção (1-5): " option

case $option in
  1)
    echo ""
    echo "📝 Fazendo commit..."
    git add -A
    git commit -m "feat: deploy - sistema de escalas para voluntários

Inclui:
- Backend Django com 4 apps completos
- Frontend React com TypeScript
- Docker Compose com 7 serviços
- GitHub Actions para deploy automático
- Documentação completa de deployment
- Correções de tipos TypeScript
- 0 erros de compilação

Docs:
- DEPLOY.md: Guia de deploy
- GITHUB_PAGES.md: GitHub Pages setup
- COMECE_AQUI.md: Quick start
- ESTRUTURA.md: Arquitetura do projeto
- README.md: Especificação técnica
"
    echo ""
    echo "✅ Commit realizado!"
    echo ""
    echo "📤 Próximo passo: git push origin main"
    ;;
    
  2)
    echo ""
    git diff --stat
    ;;
    
  3)
    echo ""
    git log --oneline -10
    ;;
    
  4)
    echo ""
    echo "Mensagem de commit customizada:"
    git add -A
    read -p "Digite a mensagem: " message
    git commit -m "$message"
    echo "✅ Commit realizado!"
    ;;
    
  5)
    echo ""
    git add -A
    echo "✅ Arquivos adicionados!"
    echo "Próximo: git commit -m 'sua mensagem'"
    ;;
    
  *)
    echo "❌ Opção inválida"
    exit 1
    ;;
esac

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  Instruções de Deploy"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Teste Local (Docker):"
echo "  docker-compose up -d"
echo "  docker-compose exec backend python manage.py createsuperuser"
echo "  Acesse: http://localhost:5173"
echo ""
echo "Deploy GitHub Pages (Frontend):"
echo "  git push origin main"
echo "  Ativa em: Settings → Pages → gh-pages"
echo "  Url: https://usuario.github.io/projeto"
echo ""
echo "Deploy Backend:"
echo "  Railway: railway.app (recommend)"
echo "  Render: render.com"
echo "  Vercel: vercel.com"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
