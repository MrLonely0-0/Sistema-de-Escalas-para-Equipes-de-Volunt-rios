#!/bin/bash

echo "🔍 Liberando porta 5173..."

# Encontra processo na porta 5173
PID=$(lsof -ti:5173)

if [ -z "$PID" ]; then
    echo "✅ Porta 5173 já está livre"
else
    echo "🔫 Matando processo $PID na porta 5173..."
    kill -9 $PID
    echo "✅ Porta liberada!"
fi

echo ""
echo "🚀 Subindo containers novamente..."
cd "$(dirname "$0")"
docker-compose up -d

echo ""
echo "⏳ Aguardando containers (30 seg)..."
sleep 30

echo ""
echo "📊 Status dos containers:"
docker-compose ps

echo ""
echo "✅ Pronto! Acesse:"
echo "   Frontend: http://localhost:5173"
echo "   Backend: http://localhost:8000"
echo "   Admin: http://localhost:8000/admin"
