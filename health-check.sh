#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}║     Sistema de Escalas para Equipes de Voluntários        ║${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"

echo -e "\n${YELLOW}📋 Verificação de Status${NC}"

# Check Docker
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker está instalado"
else
    echo -e "${RED}✗${NC} Docker não está instalado"
fi

# Check Docker Compose
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker Compose está instalado"
else
    echo -e "${RED}✗${NC} Docker Compose não está instalado"
fi

# Check Node
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v)
    echo -e "${GREEN}✓${NC} Node.js está instalado: $NODE_VERSION"
else
    echo -e "${YELLOW}⚠${NC} Node.js não está instalado (opcional se usar Docker)"
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm -v)
    echo -e "${GREEN}✓${NC} npm está instalado: $NPM_VERSION"
else
    echo -e "${YELLOW}⚠${NC} npm não está instalado (opcional se usar Docker)"
fi

echo -e "\n${YELLOW}🚀 Opções de Deploy${NC}"
echo -e "${BLUE}1)${NC} Docker Compose (Recomendado)"
echo -e "   ${GREEN}docker-compose up -d${NC}"
echo ""
echo -e "${BLUE}2)${NC} Frontend Local + Backend Docker"
echo -e "   ${GREEN}cd frontend && npm install && npm run dev${NC}"
echo ""
echo -e "${BLUE}3)${NC} Tudo Local (requer Node, npm, Python, PostgreSQL)"
echo -e "   ${GREEN}cd backend && python manage.py runserver${NC}"
echo -e "   ${GREEN}cd frontend && npm run dev${NC} (em outro terminal)"

echo -e "\n${YELLOW}📖 Documentação${NC}"
echo -e "• Setup: ${BLUE}cat SETUP.md${NC}"
echo -e "• Erros: ${BLUE}cat RESOLUCAO_ERROS.md${NC}"
echo -e "• Spec: ${BLUE}cat README.md${NC}"

echo -e "\n${GREEN}✨ Tudo pronto! Escolha uma opção acima.${NC}\n"
