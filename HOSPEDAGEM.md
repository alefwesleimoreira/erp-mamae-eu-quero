# 🌐 Guia Completo de Hospedagem

## 🎯 Escolha sua opção

| Opção | Custo | Dificuldade | Melhor para |
|-------|-------|-------------|-------------|
| Render + Vercel | **GRÁTIS** | ⭐ Fácil | Começar, testes, MVP |
| Railway | $5/mês | ⭐ Fácil | Deploy rápido |
| VPS (DigitalOcean) | $6/mês | ⭐⭐ Médio | Produção, controle total |
| AWS/GCP | Variável | ⭐⭐⭐ Difícil | Empresarial |

---

## 🆓 Opção 1: GRÁTIS - Render + Vercel

### **Parte 1: Backend no Render**

#### 1. Preparar o código
```bash
cd backend

# Adicionar gunicorn ao requirements.txt
echo "gunicorn==21.2.0" >> requirements.txt

# Criar Procfile (opcional)
echo "web: gunicorn run:app" > Procfile
```

#### 2. Fazer upload no GitHub
```bash
# Se ainda não tem repositório
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/seu-usuario/seu-repo.git
git push -u origin main
```

#### 3. Deploy no Render

1. Acesse: https://render.com
2. Cadastre-se (gratuito)
3. **Criar PostgreSQL**:
   - Click "New +" → "PostgreSQL"
   - Name: `erp-database`
   - Database: `erp_roupas_infantis`
   - User: deixe padrão
   - Region: escolha mais próximo
   - Plan: **Free**
   - Click "Create Database"
   - **COPIE** a "Internal Database URL"

4. **Criar Web Service**:
   - Click "New +" → "Web Service"
   - Connect GitHub → Selecione seu repo
   - Name: `erp-backend`
   - Region: mesma do banco
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`
   - Plan: **Free**
   
5. **Adicionar Environment Variables**:
   ```
   DATABASE_URL = <cole_a_Internal_Database_URL>
   SECRET_KEY = sua-chave-secreta-super-segura-123
   JWT_SECRET_KEY = sua-chave-jwt-super-segura-456
   FLASK_ENV = production
   PYTHONUNBUFFERED = 1
   ```

6. Click "Create Web Service"

7. **Aguarde o deploy** (5-10 minutos)

8. **Inicializar banco** (uma vez):
   - No dashboard do Render, vá em "Shell"
   - Execute:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   python seed_data.py
   ```

9. **Copie a URL** do seu backend (ex: `https://erp-backend-xxxx.onrender.com`)

### **Parte 2: Frontend no Vercel**

#### 1. Configurar API URL
```bash
cd frontend

# Criar arquivo de ambiente de produção
cat > .env.production << EOF
REACT_APP_API_URL=https://erp-backend-xxxx.onrender.com
EOF
```

#### 2. Atualizar código para usar variável de ambiente

Edite `frontend/src/App.jsx`:
```javascript
// Troque
const api = axios.create({
  baseURL: 'http://localhost:5000/api'
});

// Por
const api = axios.create({
  baseURL: (process.env.REACT_APP_API_URL || 'http://localhost:5000') + '/api'
});
```

#### 3. Fazer push das mudanças
```bash
git add .
git commit -m "Configure production API URL"
git push
```

#### 4. Deploy no Vercel

1. Acesse: https://vercel.com
2. Cadastre-se com GitHub
3. Click "Add New..." → "Project"
4. Import seu repositório
5. Configure:
   - Framework Preset: `Create React App`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`
6. Environment Variables:
   ```
   REACT_APP_API_URL = https://erp-backend-xxxx.onrender.com
   ```
7. Click "Deploy"

8. **Pronto!** Seu site está no ar 🎉

**URL final**: `https://seu-projeto.vercel.app`

---

## 💰 Opção 2: Railway ($5/mês)

### Mais simples que tudo!

1. Acesse: https://railway.app
2. Cadastre com GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Railway detecta automaticamente Python + React
5. Adiciona PostgreSQL automaticamente
6. **Deploy automático!**

**Vantagens**: Mais rápido, banco + backend + frontend juntos

---

## 🖥️ Opção 3: VPS (DigitalOcean, Vultr, Linode)

### **Passo a Passo Completo**

#### 1. Criar Droplet/VPS

**DigitalOcean** (Recomendado):
1. Acesse: https://digitalocean.com
2. Create → Droplets
3. Escolha:
   - Image: **Ubuntu 22.04 LTS**
   - Plan: **Basic $6/mês** (1GB RAM)
   - Datacenter: Mais próximo do Brasil (NY ou Toronto)
   - Authentication: SSH Key (mais seguro) ou Password
4. Create Droplet
5. **Copie o IP** do servidor

#### 2. Apontar Domínio (Opcional)

Se você tem um domínio (ex: comprado no Registro.br, GoDaddy):

1. Vá nas configurações DNS
2. Adicione registro A:
   ```
   Type: A
   Name: @
   Value: <IP_DO_SEU_VPS>
   TTL: 3600
   ```
3. Adicione também www:
   ```
   Type: A
   Name: www
   Value: <IP_DO_SEU_VPS>
   TTL: 3600
   ```

#### 3. Conectar ao servidor

```bash
# Substitua pelo seu IP
ssh root@seu-ip-aqui

# Se usar SSH key:
ssh -i sua-chave.pem root@seu-ip-aqui
```

#### 4. Upload do projeto

**Opção A - Git (Recomendado)**:
```bash
# No servidor
cd /var/www
git clone https://github.com/seu-usuario/seu-repo.git erp-roupas-infantis
```

**Opção B - SCP**:
```bash
# No seu computador
scp -r erp-roupas-infantis root@seu-ip:/var/www/
```

#### 5. Executar script de deploy

```bash
# No servidor
cd /var/www/erp-roupas-infantis
chmod +x deploy-vps.sh
./deploy-vps.sh
```

O script faz tudo automaticamente! ✅

#### 6. Acessar seu site

- **HTTP**: `http://seu-ip` ou `http://seu-dominio.com`
- **Backend API**: `http://seu-ip/api`

#### 7. Configurar SSL (HTTPS) - IMPORTANTE!

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado SSL (GRÁTIS)
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Responda as perguntas
# Email: seu@email.com
# Termos: A (Agree)
# Compartilhar email: N (No)
# Redirect HTTP to HTTPS: 2 (Yes)
```

Agora seu site tem **HTTPS** (cadeado verde) 🔒

---

## 🔧 Manutenção e Comandos Úteis

### **No VPS:**

```bash
# Ver logs do backend
sudo journalctl -u erp-backend -f

# Reiniciar backend
sudo systemctl restart erp-backend

# Reiniciar Nginx
sudo systemctl restart nginx

# Atualizar código (se usar Git)
cd /var/www/erp-roupas-infantis
git pull
sudo systemctl restart erp-backend
cd frontend && npm run build

# Ver status dos serviços
sudo systemctl status erp-backend
sudo systemctl status nginx
sudo systemctl status postgresql

# Backup do banco
sudo -u postgres pg_dump erp_roupas_infantis > backup.sql

# Restaurar banco
sudo -u postgres psql erp_roupas_infantis < backup.sql
```

### **No Render/Vercel:**

- **Atualizar**: Apenas faça `git push`, deploy é automático!
- **Logs**: Dashboard → Service → Logs
- **Variáveis**: Dashboard → Environment

---

## 💡 Dicas Importantes

### **1. Segurança**

```bash
# Altere as senhas padrão!
# No .env:
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)

# PostgreSQL: use senha forte
# Nunca comite .env no Git!
```

### **2. Firewall (VPS)**

```bash
# Configurar UFW
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### **3. Backups Automáticos**

```bash
# Criar script de backup
cat > /root/backup-db.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
sudo -u postgres pg_dump erp_roupas_infantis > /root/backups/db_$DATE.sql
find /root/backups -mtime +7 -delete
EOF

chmod +x /root/backup-db.sh

# Agendar com cron (diário às 3h)
crontab -e
# Adicione:
0 3 * * * /root/backup-db.sh
```

### **4. Monitoramento**

- **Render**: Tem dashboard com métricas
- **VPS**: Use htop (`sudo apt install htop`)
- **Uptime**: Use UptimeRobot (grátis) para monitorar se site caiu

---

## 🎯 Qual escolher?

### Começando/Teste:
✅ **Render + Vercel** (Grátis, rápido, fácil)

### Pequeno negócio:
✅ **Railway** ($5/mês, mais estável que grátis)

### Crescendo:
✅ **VPS DigitalOcean** ($6/mês, controle total)

### Empresa grande:
✅ **AWS/GCP** (escalável, caro, complexo)

---

## 🆘 Problemas Comuns

### "Cannot connect to database"
- Verifique DATABASE_URL nas variáveis de ambiente
- No Render: Use "Internal Database URL", não "External"

### "CORS Error"
- Adicione domínio do frontend no backend (config.py):
```python
CORS(app, origins=['https://seu-frontend.vercel.app'])
```

### Site lento no Render Free
- Render Free "hiberna" após 15min inatividade
- Primeira requisição demora ~30s
- Solução: Upgrade para plano pago ($7/mês)

### SSL não funciona
- Aguarde propagação DNS (até 48h)
- Verifique se domínio aponta para IP correto
- Execute certbot novamente

---

## 📞 Suporte

Precisa de ajuda? Deixe seu comentário com:
- Qual opção escolheu
- Mensagem de erro completa
- Prints da tela

Boa sorte com o deploy! 🚀
