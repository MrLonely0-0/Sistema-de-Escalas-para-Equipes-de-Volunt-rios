# GitHub Pages Deploy - Sistema de Escalas

## Configuração Automática com GitHub Actions

Este repositório está configurado para fazer deploy automático do frontend React no GitHub Pages.

### ✅ Como Funciona

1. **Trigger**: Quando você faz push na branch `main` com mudanças na pasta `frontend/`
2. **Build**: GitHub Actions roda `npm run build` gerando os arquivos estáticos em `frontend/dist/`
3. **Deploy**: Os arquivos são enviados para a branch `gh-pages` automaticamente
4. **Resultado**: Seu frontend fica disponível em `https://MeuUsuario.github.io/Sistema-de-Escalas-para-Equipes-de-Voluntários`

### 🚀 Próximos Passos

#### 1. Ativar GitHub Pages

No GitHub:
1. Vá para **Settings** → **Pages**
2. Em "Build and deployment", escolha:
   - Source: **Deploy from a branch**
   - Branch: **gh-pages** (será criada automaticamente)
   - Folder: **/ (root)**
3. Clique em **Save**

#### 2. Fazer Commit e Push

```bash
# Na raiz do projeto
git add -A
git commit -m "feat: setup github pages deploy"
git push origin main
```

#### 3. Acompanhar o Deploy

1. Vá para **Actions** no GitHub
2. Veja o workflow "Deploy Frontend to GitHub Pages" rodando
3. Após ~2 minutos, clique em **Pages** para ver o link da sua aplicação

### 🔗 URL de Deploy

Após a ativação, seu site estará disponível em:
```
https://MeuUsuario.github.io/Sistema-de-Escalas-para-Equipes-de-Voluntários
```

### ⚙️ Configurações

Se quiser usar um domínio customizado:

1. Edite `.github/workflows/deploy.yml`
2. Descomente a linha `cname: escalas.seu-dominio.com`
3. Substitua pelo seu domínio real
4. Configure DNS no seu registrador para apontar para GitHub Pages

### 📝 Variáveis de Ambiente

O frontend está configurado para chamar a API em produção:
```
VITE_API_URL = 'https://api.seu-dominio.com/api'
```

**Importante**: O backend Django deve estar publicado em um servidor separado (Vercel, Railway, Heroku, etc).

### 🔄 Deploy Local para Teste

Para testar antes de fazer push:

```bash
cd frontend
npm run build
npm run preview
# Acesse http://localhost:4173
```

### ✨ Troubleshooting

**Erro: "Page build failure"**
- Verifique se há um `vite.config.ts` válido
- Confirme que `package.json` tem os scripts `build` e `dev`
- Verifique logs em Actions → Workflow

**Blank page**
- Verifique o console do navegador (F12)
- Confirme que `VITE_API_URL` está correto
- Teste local primeiro com `npm run dev`

**API não responde**
- O backend precisa estar em outro servidor (não no GitHub Pages)
- Adicione headers CORS no backend Django

---

**Tudo pronto! Faça o push e acompanhe o deploy em Actions → Pages** 🎉
