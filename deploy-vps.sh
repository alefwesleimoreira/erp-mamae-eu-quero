#!/bin/bash

echo "🚀 Deploy ERP Roupas Infantis - VPS Setup"
echo "=========================================="

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt-get update
sudo apt-get upgrade -y

# Instalar dependências
echo "📦 Instalando dependências..."
sudo apt-get install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx nodejs npm git

# Configurar PostgreSQL
echo "🗄️ Configurando PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE erp_roupas_infantis;"
sudo -u postgres psql -c "CREATE USER erpuser WITH PASSWORD 'senha_segura_aqui';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE erp_roupas_infantis TO erpuser;"

# Clonar ou copiar projeto
echo "📁 Configurando projeto..."
cd /var/www/
sudo mkdir -p erp-roupas-infantis
sudo chown -R $USER:$USER erp-roupas-infantis
cd erp-roupas-infantis

# Backend
echo "🐍 Configurando Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Criar .env
cat > .env << EOF
DATABASE_URL=postgresql://erpuser:senha_segura_aqui@localhost/erp_roupas_infantis
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
FLASK_ENV=production
EOF

# Inicializar banco
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed_data.py

# Criar serviço systemd para backend
echo "⚙️ Criando serviço systemd..."
sudo tee /etc/systemd/system/erp-backend.service > /dev/null << EOF
[Unit]
Description=ERP Backend Gunicorn
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=/var/www/erp-roupas-infantis/backend
Environment="PATH=/var/www/erp-roupas-infantis/backend/venv/bin"
ExecStart=/var/www/erp-roupas-infantis/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 run:app

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl start erp-backend
sudo systemctl enable erp-backend

# Frontend
echo "⚛️ Configurando Frontend..."
cd ../frontend
npm install
npm run build

# Configurar Nginx
echo "🌐 Configurando Nginx..."
sudo tee /etc/nginx/sites-available/erp-roupas << EOF
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    # Frontend (React build)
    location / {
        root /var/www/erp-roupas-infantis/frontend/build;
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/erp-roupas /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# SSL com Let's Encrypt (opcional)
echo "🔒 Configurando SSL (certifique-se de que o domínio está apontado)..."
read -p "Deseja configurar SSL agora? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]
then
    sudo apt-get install -y certbot python3-certbot-nginx
    read -p "Digite seu domínio (ex: exemplo.com): " DOMAIN
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN
fi

echo "✅ Deploy concluído!"
echo "🌐 Seu site está rodando!"
echo "📝 Backend: http://seu-ip:5000"
echo "📝 Frontend: http://seu-ip"
echo ""
echo "🔧 Comandos úteis:"
echo "  - Ver logs backend: sudo journalctl -u erp-backend -f"
echo "  - Reiniciar backend: sudo systemctl restart erp-backend"
echo "  - Reiniciar nginx: sudo systemctl restart nginx"
