# 🚀 Guia de Início Rápido

Este guia irá ajudá-lo a configurar e executar o sistema rapidamente.

## ⚡ Setup Rápido (5 minutos)

### 1. Clone ou baixe o projeto
```bash
cd erp-roupas-infantis
```

### 2. Configure o PostgreSQL

**Opção A - PostgreSQL Local:**
```bash
# Instale PostgreSQL
# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# macOS (com Homebrew):
brew install postgresql

# Windows: Baixe do site oficial

# Crie o banco
sudo -u postgres createdb erp_roupas_infantis
```

**Opção B - PostgreSQL com Docker:**
```bash
docker run --name postgres-erp \
  -e POSTGRES_PASSWORD=senha123 \
  -e POSTGRES_DB=erp_roupas_infantis \
  -p 5432:5432 \
  -d postgres:14
```

### 3. Configure o Backend

```bash
cd backend

# Crie ambiente virtual Python
python3 -m venv venv

# Ative o ambiente
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env

# Edite .env com suas credenciais do PostgreSQL
# Exemplo:
# DATABASE_URL=postgresql://postgres:senha123@localhost/erp_roupas_infantis
```

### 4. Inicialize o Banco

```bash
# Dentro de backend/ com venv ativado

# Criar estrutura do banco
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Popular com dados de exemplo
python seed_data.py
```

### 5. Inicie o Backend

```bash
# Ainda em backend/
python run.py
```

✅ Backend rodando em `http://localhost:5000`

### 6. Configure o Frontend

**Em um novo terminal:**

```bash
cd frontend

# Instale dependências
npm install

# Inicie o servidor
npm start
```

✅ Frontend rodando em `http://localhost:3000`

## 🎯 Acessando o Sistema

### E-commerce (Loja Virtual)
- URL: `http://localhost:3000`
- Navegue pelos produtos
- Visualize categorias

### Painel Administrativo
- URL: `http://localhost:3000/admin`
- **Login Admin:**
  - Email: `admin@loja.com`
  - Senha: `admin123`
- **Login Vendedor:**
  - Email: `vendedor@loja.com`
  - Senha: `vendedor123`

## 📊 Explorando o Dashboard

Após fazer login como admin, você verá:

1. **Dashboard Principal** - Métricas de vendas, crescimento, ticket médio
2. **Produtos** - Catálogo completo, estoque, preços
3. **Vendas** - Histórico de pedidos e status
4. **Clientes** - Cadastro e dados
5. **Financeiro** - Fluxo de caixa, receitas e despesas

## 🧪 Testando Funcionalidades

### Criar um Produto
1. Acesse `/admin/produtos`
2. Clique em "Novo Produto"
3. Preencha os dados
4. Salve

### Registrar uma Venda
1. Acesse `/admin/vendas`
2. Clique em "Nova Venda"
3. Selecione cliente e produtos
4. Finalize

### Ver Relatórios
1. Acesse `/admin` (Dashboard)
2. Visualize gráficos de vendas
3. Veja produtos mais vendidos
4. Analise métricas

## 🔧 Comandos Úteis

### Backend
```bash
# Resetar banco e repopular
python seed_data.py

# Criar nova migração
flask db migrate -m "descrição"

# Aplicar migrações
flask db upgrade

# Reverter migração
flask db downgrade
```

### Frontend
```bash
# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install

# Build para produção
npm run build
```

## 🐛 Problemas Comuns

### Erro de conexão com PostgreSQL
```bash
# Verifique se PostgreSQL está rodando
sudo service postgresql status  # Linux
brew services list  # macOS

# Verifique a URL no .env
DATABASE_URL=postgresql://usuario:senha@localhost/erp_roupas_infantis
```

### Porta 5000 ou 3000 em uso
```bash
# Mude a porta no backend (run.py):
app.run(port=5001)

# Mude a porta do frontend:
PORT=3001 npm start
```

### Erro "Module not found"
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## 📱 Próximos Passos

1. ✅ Personalize as cores em `frontend/tailwind.config.js`
2. ✅ Adicione seu logo em `frontend/public/`
3. ✅ Configure gateway de pagamento
4. ✅ Integre com sistema de envio
5. ✅ Configure emails transacionais

## 🆘 Suporte

- 📧 Email: suporte@loja.com
- 📝 Issues: GitHub Issues
- 📖 Docs: README.md completo

---

**Pronto! Seu sistema está funcionando! 🎉**

Explore as funcionalidades e personalize conforme suas necessidades.
