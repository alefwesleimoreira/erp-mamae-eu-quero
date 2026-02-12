# 🛍️ ERP e E-commerce para Loja de Roupas Infantis

Sistema completo de gestão empresarial (ERP) integrado com e-commerce para lojas de roupas infantis. Desenvolvido com Python Flask + PostgreSQL + React.

## 📋 Funcionalidades

### 🏪 E-commerce (Loja Virtual)
- ✅ Catálogo de produtos com filtros
- ✅ Carrinho de compras
- ✅ Sistema de categorias
- ✅ Busca de produtos
- ✅ Gestão de variações (tamanhos, cores)
- ✅ Imagens de produtos
- ✅ Área do cliente

### 💼 ERP (Gestão Interna)
- ✅ **Dashboard com BI**: Métricas, gráficos e análises
- ✅ **Gestão de Produtos**: Cadastro completo com estoque
- ✅ **Controle de Estoque**: Movimentações e alertas
- ✅ **Gestão de Vendas**: PDV e controle de pedidos
- ✅ **Clientes**: Cadastro e histórico
- ✅ **Fornecedores**: Gerenciamento completo
- ✅ **Fluxo de Caixa**: Receitas, despesas e relatórios
- ✅ **Relatórios Analíticos**: Vendas, produtos, categorias

### 📊 Business Intelligence
- Vendas por período (dia/semana/mês)
- Produtos mais vendidos
- Vendas por categoria e gênero
- Taxa de conversão
- Análise de crescimento
- Alertas de estoque baixo

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.10+**
- **Flask** - Framework web
- **SQLAlchemy** - ORM
- **PostgreSQL** - Banco de dados
- **Flask-JWT-Extended** - Autenticação
- **Flask-CORS** - CORS
- **Flask-Migrate** - Migrações

### Frontend
- **React 18** - Interface
- **React Router** - Navegação
- **Axios** - Requisições HTTP
- **Tailwind CSS** - Estilização
- **Recharts** - Gráficos
- **React Icons** - Ícones

## 📦 Instalação

### 1. Pré-requisitos
```bash
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
```

### 2. Configurar Banco de Dados
```bash
# Criar banco de dados PostgreSQL
createdb erp_roupas_infantis

# Ou via psql
psql -U postgres
CREATE DATABASE erp_roupas_infantis;
\q
```

### 3. Backend
```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Inicializar banco de dados
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Executar servidor
python run.py
```

Backend rodará em: `http://localhost:5000`

### 4. Frontend
```bash
cd frontend

# Instalar dependências
npm install

# Executar servidor de desenvolvimento
npm start
```

Frontend rodará em: `http://localhost:3000`

## 🗄️ Estrutura do Banco de Dados

### Principais Tabelas:
- **usuarios** - Autenticação e permissões
- **clientes** - Dados dos clientes
- **fornecedores** - Cadastro de fornecedores
- **produtos** - Catálogo de produtos
- **categorias** - Categorias de produtos
- **produto_variacao** - Tamanhos e cores
- **vendas** - Pedidos e vendas
- **item_venda** - Itens de cada venda
- **movimentacao_estoque** - Controle de estoque
- **financeiro** - Fluxo de caixa

## 🔐 Autenticação

O sistema usa JWT (JSON Web Tokens) para autenticação:

```javascript
// Login
POST /api/auth/login
{
  "email": "usuario@email.com",
  "senha": "senha123"
}

// Retorna:
{
  "access_token": "...",
  "refresh_token": "...",
  "usuario": {...}
}
```

## 📡 API Endpoints

### Autenticação
- `POST /api/auth/register` - Registrar usuário
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Renovar token
- `GET /api/auth/me` - Dados do usuário logado

### Produtos
- `GET /api/produtos` - Listar produtos (público)
- `GET /api/produtos/:id` - Detalhes do produto
- `POST /api/produtos` - Criar produto (admin)
- `PUT /api/produtos/:id` - Atualizar produto (admin)
- `DELETE /api/produtos/:id` - Deletar produto (admin)

### Vendas
- `GET /api/vendas` - Listar vendas
- `GET /api/vendas/:id` - Detalhes da venda
- `POST /api/vendas` - Criar venda
- `PATCH /api/vendas/:id/status` - Atualizar status

### Dashboard
- `GET /api/dashboard/resumo` - Métricas gerais
- `GET /api/dashboard/vendas-por-periodo` - Vendas por período
- `GET /api/dashboard/produtos-mais-vendidos` - Top produtos
- `GET /api/dashboard/vendas-por-categoria` - Vendas por categoria

### Financeiro
- `GET /api/financeiro/lancamentos` - Listar lançamentos
- `POST /api/financeiro/lancamentos` - Criar lançamento
- `GET /api/financeiro/fluxo-caixa` - Resumo financeiro

### Clientes
- `GET /api/clientes` - Listar clientes
- `GET /api/clientes/:id` - Detalhes do cliente
- `POST /api/clientes` - Criar cliente

### Estoque
- `GET /api/estoque/movimentacoes` - Movimentações
- `GET /api/estoque/alertas` - Alertas de estoque baixo

## 👥 Tipos de Usuário

1. **Admin** - Acesso completo ao sistema
2. **Vendedor** - Gestão de vendas e produtos
3. **Cliente** - Acesso ao e-commerce

## 🎨 Personalização

### Cores (Tailwind)
Edite `frontend/tailwind.config.js` para personalizar as cores:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Suas cores aqui
      }
    }
  }
}
```

### Logo e Imagens
Substitua os ícones e imagens em:
- `frontend/public/` - Logo e favicon
- `frontend/src/assets/` - Imagens internas

## 📈 Próximas Funcionalidades

- [ ] Gateway de pagamento (Stripe, PagSeguro)
- [ ] Envio de emails (confirmação de pedidos)
- [ ] Relatórios em PDF
- [ ] Sistema de cupons de desconto
- [ ] Avaliações de produtos
- [ ] Rastreamento de envio
- [ ] App mobile (React Native)
- [ ] Integração com redes sociais

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Suporte

Para dúvidas e suporte:
- Abra uma issue no GitHub
- Email: suporte@loja.com

---

Desenvolvido com ❤️ para facilitar a gestão de lojas de roupas infantis
