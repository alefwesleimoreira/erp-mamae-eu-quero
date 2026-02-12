#!/bin/bash

echo "🔧 Script de Correção - Estrutura GitHub ERP"
echo "=============================================="
echo ""
echo "Este script vai reorganizar seu repositório na estrutura correta."
echo ""
read -p "Você está na raiz do repositório erp-mamae-eu-quero? (s/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[SsYy]$ ]]
then
    echo "❌ Execute este script na raiz do repositório!"
    exit 1
fi

echo ""
echo "⚠️  ATENÇÃO: Este script vai mover arquivos."
echo "   Recomendo fazer backup primeiro!"
echo ""
read -p "Continuar? (s/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[SsYy]$ ]]
then
    echo "Operação cancelada."
    exit 1
fi

echo ""
echo "🚀 Iniciando reorganização..."
echo ""

# Criar estrutura de diretórios
echo "📁 Criando estrutura de pastas..."
mkdir -p backend frontend docs

# Mover arquivos do BACKEND
echo "🐍 Movendo arquivos do backend..."
[ -d "app" ] && mv app backend/ 2>/dev/null
[ -f "config.py" ] && mv config.py backend/ 2>/dev/null
[ -f "run.py" ] && mv run.py backend/ 2>/dev/null
[ -f "seed_data.py" ] && mv seed_data.py backend/ 2>/dev/null
[ -f "requirements.txt" ] && mv requirements.txt backend/ 2>/dev/null
[ -d "migrations" ] && mv migrations backend/ 2>/dev/null

# Dockerfile do backend
if [ -f "Dockerfile" ]; then
    # Verificar se é Dockerfile do backend (contém Python)
    if grep -q "python" Dockerfile 2>/dev/null; then
        mv Dockerfile backend/Dockerfile 2>/dev/null
        echo "  ✓ Dockerfile movido para backend/"
    fi
fi

# Mover arquivos do FRONTEND
echo "⚛️  Movendo arquivos do frontend..."
[ -d "src" ] && mv src frontend/ 2>/dev/null
[ -d "public" ] && mv public frontend/ 2>/dev/null
[ -f "package.json" ] && mv package.json frontend/ 2>/dev/null
[ -f "tailwind.config.js" ] && mv tailwind.config.js frontend/ 2>/dev/null

# Mover documentação
echo "📚 Movendo documentação..."
[ -f "API.md" ] && mv API.md docs/ 2>/dev/null
[ -f "HOSPEDAGEM.md" ] && mv HOSPEDAGEM.md docs/ 2>/dev/null
[ -f "QUICK-START.md" ] && mv QUICK-START.md docs/ 2>/dev/null
[ -f "CHECKLIST-DEPLOY.md" ] && mv CHECKLIST-DEPLOY.md docs/ 2>/dev/null
[ -f "COMANDOS-RAPIDOS.md" ] && mv COMANDOS-RAPIDOS.md docs/ 2>/dev/null

# Remover arquivo estranho
if [ -f "erp-roupas-infantis" ]; then
    echo "🗑️  Removendo arquivo 'erp-roupas-infantis'..."
    rm erp-roupas-infantis
fi

# Criar .gitignore do backend
echo "📝 Criando backend/.gitignore..."
cat > backend/.gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Flask
instance/
.webassets-cache

# Environment
.env
.env.local

# Database
*.db
*.sqlite
migrations/

# IDE
.vscode/
.idea/
*.swp
*.swo
EOF

# Criar .env.example do backend
echo "📝 Criando backend/.env.example..."
cat > backend/.env.example << 'EOF'
# Configurações do Banco de Dados PostgreSQL
DATABASE_URL=postgresql://postgres:senha@localhost/erp_roupas_infantis

# Chaves secretas (MUDE EM PRODUÇÃO!)
SECRET_KEY=sua-chave-secreta-super-segura
JWT_SECRET_KEY=sua-chave-jwt-super-segura

# Ambiente
FLASK_ENV=development
FLASK_DEBUG=1
EOF

# Criar .gitignore do frontend
echo "📝 Criando frontend/.gitignore..."
cat > frontend/.gitignore << 'EOF'
# Dependencies
node_modules/
.pnp/
.pnp.js

# Testing
coverage/

# Production
build/
dist/

# Environment
.env
.env.local
.env.production.local

# IDE
.vscode/
.idea/

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
EOF

# Atualizar .gitignore da raiz
echo "📝 Atualizando .gitignore da raiz..."
cat > .gitignore << 'EOF'
# Backend
backend/__pycache__/
backend/venv/
backend/env/
backend/.env
backend/migrations/
backend/*.db

# Frontend
frontend/node_modules/
frontend/build/
frontend/.env
frontend/.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
*.log
EOF

# Criar index.js se não existir
if [ ! -f "frontend/src/index.js" ]; then
    echo "📝 Criando frontend/src/index.js..."
    mkdir -p frontend/src
    cat > frontend/src/index.js << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF
fi

# Criar index.css se não existir
if [ ! -f "frontend/src/index.css" ]; then
    echo "📝 Criando frontend/src/index.css..."
    cat > frontend/src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors;
  }
  
  .btn-secondary {
    @apply bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors;
  }
  
  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }
  
  .input-field {
    @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent;
  }
}
EOF
fi

# Atualizar docker-compose.yml
if [ -f "docker-compose.yml" ]; then
    echo "📝 Atualizando docker-compose.yml..."
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:14
    container_name: erp-postgres
    environment:
      POSTGRES_DB: erp_roupas_infantis
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: senha123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - erp-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: erp-backend
    environment:
      DATABASE_URL: postgresql://postgres:senha123@postgres:5432/erp_roupas_infantis
      SECRET_KEY: sua-chave-secreta
      JWT_SECRET_KEY: sua-chave-jwt
      FLASK_ENV: production
    ports:
      - "5000:5000"
    depends_on:
      - postgres
    networks:
      - erp-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: erp-frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - erp-network
    environment:
      - REACT_APP_API_URL=http://localhost:5000

networks:
  erp-network:
    driver: bridge

volumes:
  postgres_data:
EOF
fi

echo ""
echo "✅ Reorganização concluída!"
echo ""
echo "📊 Nova estrutura:"
tree -L 2 -I 'node_modules|venv|__pycache__|.git' 2>/dev/null || echo "
erp-mamae-eu-quero/
├── backend/
│   ├── app/
│   ├── config.py
│   ├── run.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/
├── README.md
└── docker-compose.yml
"

echo ""
echo "🔍 Próximos passos:"
echo ""
echo "1. Verificar se está tudo OK:"
echo "   git status"
echo ""
echo "2. Fazer commit:"
echo "   git add ."
echo "   git commit -m 'Reorganizar estrutura: backend e frontend separados'"
echo ""
echo "3. Fazer push:"
echo "   git push origin main"
echo ""
echo "4. Testar localmente:"
echo "   cd backend && python run.py"
echo "   cd frontend && npm start"
echo ""
echo "✨ Pronto para deploy no Render e Vercel!"
