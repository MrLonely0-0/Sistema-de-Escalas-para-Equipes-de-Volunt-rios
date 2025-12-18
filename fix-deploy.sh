#!/bin/bash

cd "$(dirname "$0")"

git add -A

git commit -m "fix: corrige build vite e github pages deploy

- Adiciona root e publicDir no vite.config.ts
- Adiciona base path para GitHub Pages (/repo-name/)
- Remove CNAME do workflow (usar GitHub domain)
- Adiciona permissões corretas no workflow
- Remove filtro de paths para rodar em todos os pushes
- Adiciona .nojekyll para suportar arquivos com underscore
- Force orphan branch para gh-pages limpo

Isso resolve:
- 'Could not resolve entry module' error
- GitHub Pages mostrando README em vez do app
- Paths relativos incorretos no navegador
"

git log --oneline -5

echo ""
echo "✅ Commit de correção realizado!"
echo ""
echo "🚀 Próximos passos:"
echo "1. git push origin main"
echo "2. Aguarde o workflow rodar (Actions tab)"
echo "3. Acesse: https://seuusername.github.io/Sistema-de-Escalas-para-Equipes-de-Volunt-rios/"
