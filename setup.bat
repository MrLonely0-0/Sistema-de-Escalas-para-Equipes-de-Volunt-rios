@echo off
echo 🚀 Iniciando setup do Sistema de Escalas...

echo.
echo 📦 Configurando Backend...
cd backend
copy .env.example .env

echo.
echo 📦 Configurando Frontend...
cd ..\frontend
call npm install

echo.
echo ✅ Setup concluído!
echo.
echo 📋 Próximos passos:
echo 1. Volte para a raiz do projeto: cd ..
echo 2. Inicie os serviços: docker-compose up -d
echo 3. Crie um superusuário: docker-compose exec backend python manage.py createsuperuser
echo 4. Acesse:
echo    - Frontend: http://localhost:5173
echo    - Admin: http://localhost:8000/admin
echo    - API: http://localhost:8000/api
