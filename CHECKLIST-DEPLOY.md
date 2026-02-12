# ✅ Checklist de Deploy - ERP Roupas Infantis

Use este checklist para garantir que tudo está configurado corretamente antes do deploy.

## 📋 Pré-Deploy

### Backend
- [ ] `requirements.txt` atualizado com todas dependências
- [ ] `gunicorn` adicionado ao requirements.txt
- [ ] Variáveis de ambiente configuradas (.env)
- [ ] SECRET_KEY e JWT_SECRET_KEY geradas (usar openssl rand -hex 32)
- [ ] DATABASE_URL configurada corretamente
- [ ] CORS configurado com domínio do frontend
- [ ] Arquivo `.env` NÃO está no Git (.gitignore)
- [ ] Migrations criadas (`flask db migrate`)
- [ ] Banco de dados funcionando localmente

### Frontend
- [ ] `REACT_APP_API_URL` configurada para produção
- [ ] Build funciona localmente (`npm run build`)
- [ ] Todas dependências no package.json
- [ ] Axios configurado para usar variável de ambiente
- [ ] Testes básicos funcionando

### Geral
- [ ] Código versionado no Git
- [ ] README.md atualizado
- [ ] .gitignore configurado (node_modules, venv, .env)
- [ ] Documentação básica pronta

---

## 🚀 Deploy - Render + Vercel (GRÁTIS)

### 1. PostgreSQL no Render
- [ ] Conta criada no Render.com
- [ ] PostgreSQL Database criado (plano Free)
- [ ] Internal Database URL copiada
- [ ] Database URL salva em local seguro

### 2. Backend no Render
- [ ] Repositório GitHub conectado
- [ ] Web Service criado
- [ ] Root Directory: `backend`
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `gunicorn run:app`
- [ ] Environment Variables configuradas:
  - [ ] DATABASE_URL
  - [ ] SECRET_KEY
  - [ ] JWT_SECRET_KEY
  - [ ] FLASK_ENV=production
  - [ ] PYTHONUNBUFFERED=1
- [ ] Deploy bem-sucedido (status verde)
- [ ] Banco inicializado via Shell:
  - [ ] `flask db init`
  - [ ] `flask db migrate`
  - [ ] `flask db upgrade`
  - [ ] `python seed_data.py`
- [ ] Endpoint /api/produtos retorna dados
- [ ] URL do backend copiada

### 3. Frontend no Vercel
- [ ] Conta criada no Vercel.com
- [ ] .env.production criado com REACT_APP_API_URL
- [ ] Código commitado e pushed para GitHub
- [ ] Projeto importado do GitHub
- [ ] Root Directory: `frontend`
- [ ] Framework Preset: Create React App
- [ ] Environment Variable adicionada (REACT_APP_API_URL)
- [ ] Deploy bem-sucedido
- [ ] Site carrega corretamente
- [ ] Login funciona
- [ ] Produtos carregam do backend

### 4. Testes Pós-Deploy
- [ ] Acesso ao site funciona
- [ ] Login admin funciona (admin@loja.com)
- [ ] Dashboard carrega métricas
- [ ] Lista de produtos funciona
- [ ] Criar produto funciona
- [ ] Criar venda funciona
- [ ] Imagens carregam (se houver)
- [ ] Responsividade mobile ok
- [ ] Console sem erros críticos

---

## 🖥️ Deploy - VPS (DigitalOcean/Vultr)

### 1. Servidor
- [ ] Droplet/VPS criado (Ubuntu 22.04)
- [ ] IP anotado
- [ ] SSH funcionando
- [ ] Domínio apontado para IP (opcional)
- [ ] DNS propagado (verificar com ping)

### 2. Preparação do Servidor
- [ ] Sistema atualizado (`apt update && apt upgrade`)
- [ ] Python 3 instalado
- [ ] PostgreSQL instalado
- [ ] Nginx instalado
- [ ] Node.js instalado
- [ ] Git instalado

### 3. Banco de Dados
- [ ] PostgreSQL rodando
- [ ] Database criado
- [ ] Usuário criado com senha
- [ ] Permissões concedidas
- [ ] Conexão testada

### 4. Backend
- [ ] Código copiado/clonado em /var/www/
- [ ] Virtual env criado
- [ ] Dependências instaladas
- [ ] .env configurado
- [ ] Migrations executadas
- [ ] Dados de exemplo populados
- [ ] Gunicorn instalado
- [ ] Systemd service criado e ativo
- [ ] Backend responde em localhost:5000

### 5. Frontend
- [ ] npm install executado
- [ ] .env.production configurado
- [ ] Build criado (`npm run build`)
- [ ] Build folder em /var/www/.../frontend/build

### 6. Nginx
- [ ] Configuração criada em sites-available
- [ ] Symlink criado em sites-enabled
- [ ] Configuração testada (`nginx -t`)
- [ ] Nginx reiniciado
- [ ] Site responde no IP
- [ ] API responde em /api

### 7. SSL/HTTPS (Certbot)
- [ ] Certbot instalado
- [ ] Certificado obtido para domínio
- [ ] Auto-renovação configurada
- [ ] HTTPS funciona (cadeado verde)
- [ ] Redirect HTTP → HTTPS ativo

### 8. Segurança
- [ ] Firewall configurado (UFW)
- [ ] Apenas portas necessárias abertas (80, 443, 22)
- [ ] Senha do PostgreSQL forte
- [ ] SECRET_KEY e JWT_SECRET_KEY únicos
- [ ] .env não versionado
- [ ] Backups configurados

### 9. Monitoramento
- [ ] Logs acessíveis
- [ ] Serviços configurados para auto-start
- [ ] Backup automático configurado
- [ ] Monitoramento uptime (UptimeRobot)

### 10. Testes Finais
- [ ] Site carrega via domínio
- [ ] HTTPS funciona
- [ ] Login funciona
- [ ] CRUD de produtos funciona
- [ ] Vendas funcionam
- [ ] Dashboard carrega
- [ ] Performance aceitável
- [ ] Mobile responsivo

---

## 🔄 Pós-Deploy

### Documentação
- [ ] URL do site documentada
- [ ] Credenciais de admin salvas
- [ ] Credenciais do servidor salvas
- [ ] Processo de backup documentado
- [ ] Processo de atualização documentado

### Treinamento
- [ ] Admin sabe fazer login
- [ ] Admin sabe cadastrar produtos
- [ ] Admin sabe processar vendas
- [ ] Admin sabe ver relatórios
- [ ] Admin sabe fazer backup

### Marketing
- [ ] Domínio registrado
- [ ] Email profissional configurado
- [ ] Redes sociais vinculadas
- [ ] Google Analytics/similar instalado
- [ ] Política de privacidade criada
- [ ] Termos de uso criados

---

## 🐛 Troubleshooting

### Se algo der errado:

**Backend não sobe:**
- [ ] Ver logs: `sudo journalctl -u erp-backend -f`
- [ ] Verificar DATABASE_URL
- [ ] Verificar se PostgreSQL está rodando
- [ ] Verificar permissões de arquivo

**Frontend não carrega:**
- [ ] Verificar build (erros de compilação)
- [ ] Verificar REACT_APP_API_URL
- [ ] Verificar configuração Nginx
- [ ] Ver logs Nginx: `sudo tail -f /var/log/nginx/error.log`

**CORS errors:**
- [ ] Adicionar domínio frontend no CORS (backend)
- [ ] Verificar URL da API no frontend

**Database connection failed:**
- [ ] Verificar DATABASE_URL
- [ ] PostgreSQL rodando?
- [ ] Firewall bloqueando?
- [ ] Credenciais corretas?

**SSL não funciona:**
- [ ] DNS propagado? (pode levar 48h)
- [ ] Domínio aponta para IP correto?
- [ ] Executar certbot novamente
- [ ] Verificar logs: `sudo certbot renew --dry-run`

---

## 📞 Suporte

- Email: suporte@loja.com
- GitHub Issues
- Documentação: README.md

---

**✅ Tudo checado? Parabéns, seu sistema está no ar! 🎉**

Próximos passos:
1. Configure gateway de pagamento
2. Integre envio de emails
3. Configure backup automático
4. Monitore performance
5. Colete feedback dos usuários
