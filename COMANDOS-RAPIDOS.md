# ⚡ Comandos Rápidos - Cheat Sheet

## 🚀 Deploy Rápido (Copy & Paste)

### Opção 1: Render + Vercel (GRÁTIS)

#### Backend (Render)
```bash
# Preparar projeto
cd backend
echo "gunicorn==21.2.0" >> requirements.txt
git add .
git commit -m "Add gunicorn"
git push

# No Render.com:
# 1. New PostgreSQL (copie Internal URL)
# 2. New Web Service
#    Build: pip install -r requirements.txt
#    Start: gunicorn run:app
# 3. Adicione env vars:
#    DATABASE_URL=<internal_url>
#    SECRET_KEY=sua-chave-123
#    JWT_SECRET_KEY=sua-chave-456
#    FLASK_ENV=production

# Após deploy, no Shell do Render:
flask db init
flask db migrate -m "Initial"
flask db upgrade
python seed_data.py
```

#### Frontend (Vercel)
```bash
cd frontend
echo "REACT_APP_API_URL=https://seu-backend.onrender.com" > .env.production

# Editar src/App.jsx linha ~26:
# baseURL: (process.env.REACT_APP_API_URL || 'http://localhost:5000') + '/api'

git add .
git commit -m "Configure production API"
git push

# No Vercel.com:
# 1. New Project → Import do GitHub
# 2. Root Directory: frontend
# 3. Add env var: REACT_APP_API_URL
# 4. Deploy!
```

---

### Opção 2: VPS DigitalOcean

#### Setup Inicial (5 minutos)
```bash
# Conectar ao servidor
ssh root@SEU_IP

# Executar tudo de uma vez
curl -o- https://raw.githubusercontent.com/seu-repo/deploy-vps.sh | bash

# OU manualmente:
cd /var/www
git clone https://github.com/seu-usuario/seu-repo.git erp-roupas-infantis
cd erp-roupas-infantis
chmod +x deploy-vps.sh
./deploy-vps.sh
```

#### SSL (HTTPS)
```bash
sudo certbot --nginx -d seudominio.com -d www.seudominio.com
```

---

## 🔧 Comandos Úteis

### Desenvolvimento Local

```bash
# Iniciar Backend
cd backend
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
python run.py

# Iniciar Frontend
cd frontend
npm start

# Resetar banco com dados de exemplo
cd backend
python seed_data.py

# Nova migration
flask db migrate -m "Descrição"
flask db upgrade
```

### Git
```bash
# Primeira vez
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/usuario/repo.git
git push -u origin main

# Atualizações
git add .
git commit -m "Descrição da mudança"
git push

# Ver status
git status
git log --oneline -5
```

### VPS - Manutenção

```bash
# Ver logs
sudo journalctl -u erp-backend -f           # Backend logs
sudo tail -f /var/log/nginx/error.log       # Nginx errors
sudo tail -f /var/log/nginx/access.log      # Nginx access

# Reiniciar serviços
sudo systemctl restart erp-backend
sudo systemctl restart nginx
sudo systemctl restart postgresql

# Status dos serviços
sudo systemctl status erp-backend
sudo systemctl status nginx
sudo systemctl status postgresql

# Atualizar código
cd /var/www/erp-roupas-infantis
git pull
sudo systemctl restart erp-backend
cd frontend && npm run build

# Backup banco
sudo -u postgres pg_dump erp_roupas_infantis > backup_$(date +%Y%m%d).sql

# Restaurar banco
sudo -u postgres psql erp_roupas_infantis < backup.sql

# Espaço em disco
df -h

# Memória RAM
free -h

# Processos
htop  # (instalar: sudo apt install htop)
```

### PostgreSQL

```bash
# Conectar ao PostgreSQL
sudo -u postgres psql

# Comandos dentro do psql:
\l                          # Listar databases
\c erp_roupas_infantis     # Conectar ao banco
\dt                         # Listar tabelas
\d+ produtos               # Descrever tabela
SELECT COUNT(*) FROM produtos;
\q                          # Sair

# Reset completo do banco (CUIDADO!)
sudo -u postgres dropdb erp_roupas_infantis
sudo -u postgres createdb erp_roupas_infantis
cd /var/www/erp-roupas-infantis/backend
flask db upgrade
python seed_data.py
```

### Nginx

```bash
# Testar configuração
sudo nginx -t

# Recarregar config (sem downtime)
sudo nginx -s reload

# Ver sites ativos
ls -la /etc/nginx/sites-enabled/

# Editar configuração
sudo nano /etc/nginx/sites-available/erp-roupas

# Ver logs em tempo real
sudo tail -f /var/log/nginx/access.log
```

### SSL/Certbot

```bash
# Obter certificado
sudo certbot --nginx -d seudominio.com

# Renovar manualmente
sudo certbot renew

# Testar renovação
sudo certbot renew --dry-run

# Listar certificados
sudo certbot certificates

# Configurar renovação automática (já vem configurado)
sudo systemctl status certbot.timer
```

### Firewall (UFW)

```bash
# Status
sudo ufw status

# Habilitar
sudo ufw enable

# Permitir porta
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp

# Negar porta
sudo ufw deny 3000/tcp

# Resetar firewall
sudo ufw reset
```

---

## 🐛 Debug Rápido

### Backend não responde
```bash
# 1. Verificar se está rodando
sudo systemctl status erp-backend

# 2. Ver últimos erros
sudo journalctl -u erp-backend -n 50

# 3. Tentar iniciar manualmente
cd /var/www/erp-roupas-infantis/backend
source venv/bin/activate
python run.py  # Ver erros aqui

# 4. Verificar banco
sudo -u postgres psql -c "SELECT 1"
```

### Frontend não carrega
```bash
# 1. Verificar build
cd /var/www/erp-roupas-infantis/frontend
npm run build

# 2. Verificar Nginx
sudo nginx -t
sudo systemctl status nginx

# 3. Ver logs
sudo tail -f /var/log/nginx/error.log

# 4. Verificar permissões
ls -la build/
```

### CORS Error
```bash
# Backend: config.py
# Adicionar:
from flask_cors import CORS
CORS(app, origins=['https://seu-frontend.vercel.app'])

# Reiniciar
sudo systemctl restart erp-backend
```

### Database Error
```bash
# 1. PostgreSQL rodando?
sudo systemctl status postgresql

# 2. Testar conexão
psql "postgresql://usuario:senha@localhost/erp_roupas_infantis"

# 3. Verificar .env
cat /var/www/erp-roupas-infantis/backend/.env

# 4. Recriar migrations
cd backend
rm -rf migrations
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

---

## 📊 Monitoramento

### Verificar uptime
```bash
uptime
```

### Verificar disco
```bash
df -h
du -sh /var/www/erp-roupas-infantis/*
```

### Verificar memória
```bash
free -h
```

### Verificar CPU/Processos
```bash
top
htop  # Melhor, instalar com: sudo apt install htop
```

### Verificar logs de acesso
```bash
# Últimos 100 acessos
sudo tail -n 100 /var/log/nginx/access.log

# Acessos de hoje
sudo grep "$(date +%d/%b/%Y)" /var/log/nginx/access.log

# IPs mais ativos
sudo awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -10
```

---

## 🔐 Segurança

### Gerar chaves seguras
```bash
# SECRET_KEY
openssl rand -hex 32

# JWT_SECRET_KEY
openssl rand -hex 32

# Senha PostgreSQL
openssl rand -base64 32
```

### Verificar portas abertas
```bash
sudo netstat -tulpn | grep LISTEN
sudo ss -tulpn
```

### Verificar tentativas de login SSH
```bash
sudo grep "Failed password" /var/log/auth.log
```

### Alterar senha PostgreSQL
```bash
sudo -u postgres psql
ALTER USER erpuser WITH PASSWORD 'nova_senha_super_segura';
\q
```

---

## 📱 URLs Importantes

### Desenvolvimento
- Backend: http://localhost:5000
- Frontend: http://localhost:3000
- Docs API: http://localhost:5000/api/

### Produção (exemplos)
- Site: https://seudominio.com
- API: https://seudominio.com/api
- Admin: https://seudominio.com/admin

### Ferramentas
- Render: https://dashboard.render.com
- Vercel: https://vercel.com/dashboard
- DigitalOcean: https://cloud.digitalocean.com
- GitHub: https://github.com/seu-usuario/seu-repo

---

## 🆘 Emergency - Site Caiu!

```bash
# 1. Verificar serviços
sudo systemctl status erp-backend nginx postgresql

# 2. Reiniciar tudo
sudo systemctl restart erp-backend
sudo systemctl restart nginx
sudo systemctl restart postgresql

# 3. Ver logs
sudo journalctl -u erp-backend -f

# 4. Se não resolver, reverter deploy
cd /var/www/erp-roupas-infantis
git log --oneline -5
git checkout COMMIT_ANTERIOR
sudo systemctl restart erp-backend

# 5. Ainda não? Chamar backup!
sudo -u postgres psql erp_roupas_infantis < backup_ultimo.sql
```

---

## 📞 Ajuda Rápida

**Erro "ModuleNotFoundError":**
```bash
pip install -r requirements.txt
```

**Erro "npm ERR!":**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Porta já em uso:**
```bash
# Ver processo na porta 5000
sudo lsof -i :5000
# Matar processo
sudo kill -9 PID
```

**Permissão negada:**
```bash
sudo chown -R $USER:$USER /var/www/erp-roupas-infantis
chmod +x arquivo.sh
```

---

Salve este arquivo para consulta rápida! 🚀
