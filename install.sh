#!/bin/bash

# Script para instalar todas as dependências

echo "🚀 Instalando Sistema de Escalas para Voluntários..."
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Frontend
echo -e "${BLUE}📦 Instalando dependências do Frontend...${NC}"
cd frontend
npm install
cd ..

echo ""
echo -e "${BLUE}📦 Instalando dependências do Backend...${NC}"
cd backend
pip install -r requirements.txt
cd ..

echo ""
echo -e "${GREEN}✅ Instalação concluída!${NC}"
echo ""
echo "Próximos passos:"
echo "1. docker-compose up -d"
echo "2. docker-compose exec backend python manage.py createsuperuser"
echo "3. Abra http://localhost:5173 (frontend) ou http://localhost:8000/admin (admin)"
