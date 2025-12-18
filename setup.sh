#!/bin/bash

echo "🚀 Iniciando setup do Sistema de Escalas..."

# Backend setup
echo -e "\n📦 Configurando Backend..."
cd backend
cp .env.example .env

# Frontend setup
echo -e "\n📦 Configurando Frontend..."
cd ../frontend
npm install

echo -e "\n✅ Setup concluído!"
echo -e "\n📋 Próximos passos:"
echo "1. Volte para a raiz do projeto: cd .."
echo "2. Inicie os serviços: docker-compose up -d"
echo "3. Crie um superusuário: docker-compose exec backend python manage.py createsuperuser"
echo "4. Acesse:"
echo "   - Frontend: http://localhost:5173"
echo "   - Admin: http://localhost:8000/admin"
echo "   - API: http://localhost:8000/api"
