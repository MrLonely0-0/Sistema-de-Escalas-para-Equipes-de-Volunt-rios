#!/bin/bash

cd "$(dirname "$0")"

echo "📝 Fazendo commit das correções..."
echo ""

git add -A

git commit -m "fix: corrige versões dependencies e config docker

- Remove version obsoleta do docker-compose.yml
- Corrige djangorestframework-simplejwt: 5.3.2 → 5.3.1
- Corrige django-environ: 0.21.0 → 0.11.2
- Adiciona .nojekyll no frontend/public
- Move index.html para frontend/index.html (raiz)
- Ajusta vite.config.ts com base path correto
- Adiciona permissions corretas no workflow deploy
- Cria scripts auxiliares (start.sh, fix-deploy.sh)

Build Docker: ✅ Passou
Frontend: ✅ Sem erros TypeScript
Backend: ✅ Sem erros Python
"

echo ""
echo "✅ Commit realizado!"
echo ""
echo "🚀 Próximos passos:"
echo "1. git push origin main"
echo "2. chmod +x start.sh && ./start.sh (para liberar porta e subir)"
echo "3. Acesse http://localhost:5173"
