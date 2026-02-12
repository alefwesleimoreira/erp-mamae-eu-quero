# 📡 Documentação da API

Base URL: `http://localhost:5000/api`

## 🔐 Autenticação

A API usa JWT (JSON Web Tokens). Após o login, inclua o token no header:
```
Authorization: Bearer {seu_token}
```

### POST /auth/register
Registrar novo usuário

**Request:**
```json
{
  "nome": "Nome Completo",
  "email": "email@example.com",
  "senha": "senha123",
  "telefone": "(11) 99999-9999",
  "cpf": "123.456.789-00"
}
```

**Response (201):**
```json
{
  "mensagem": "Usuário criado com sucesso",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "usuario": {
    "id": 1,
    "nome": "Nome Completo",
    "email": "email@example.com",
    "tipo": "cliente"
  }
}
```

### POST /auth/login
Fazer login

**Request:**
```json
{
  "email": "admin@loja.com",
  "senha": "admin123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "usuario": {
    "id": 1,
    "nome": "Administrador",
    "email": "admin@loja.com",
    "tipo": "admin"
  }
}
```

### GET /auth/me
Obter dados do usuário logado (requer autenticação)

**Response (200):**
```json
{
  "id": 1,
  "nome": "Administrador",
  "email": "admin@loja.com",
  "tipo": "admin",
  "ativo": true
}
```

---

## 📦 Produtos

### GET /produtos
Listar produtos (público)

**Query Parameters:**
- `categoria_id` (int) - Filtrar por categoria
- `genero` (string) - masculino, feminino, unissex
- `faixa_etaria` (string) - Ex: "0-3m", "1-2a"
- `q` (string) - Busca por nome/descrição
- `destaque` (boolean) - Produtos em destaque
- `ordem` (string) - recentes, preco_asc, preco_desc, nome
- `page` (int) - Página (padrão: 1)
- `per_page` (int) - Itens por página (padrão: 20)

**Response (200):**
```json
{
  "produtos": [
    {
      "id": 1,
      "codigo": "BODY001",
      "nome": "Body Manga Longa Listrado",
      "descricao": "Body confortável em algodão...",
      "slug": "body-manga-longa-listrado",
      "preco_venda": 35.00,
      "preco_promocional": null,
      "estoque_disponivel": true,
      "destaque": false,
      "genero": "unissex",
      "faixa_etaria": "0-3m",
      "imagem": "https://...",
      "categorias": [
        {"id": 1, "nome": "Bodies"}
      ]
    }
  ],
  "total": 50,
  "paginas": 3,
  "pagina_atual": 1,
  "por_pagina": 20
}
```

### GET /produtos/{id}
Obter detalhes do produto

**Response (200):**
```json
{
  "id": 1,
  "codigo": "BODY001",
  "nome": "Body Manga Longa Listrado",
  "descricao": "Body confortável em algodão...",
  "slug": "body-manga-longa-listrado",
  "genero": "unissex",
  "faixa_etaria": "0-3m",
  "preco_venda": 35.00,
  "preco_promocional": null,
  "estoque_atual": 50,
  "peso": 0.15,
  "dimensoes": {
    "altura": 30.0,
    "largura": 20.0,
    "profundidade": 5.0
  },
  "imagens": [
    {
      "id": 1,
      "url": "https://...",
      "principal": true,
      "ordem": 0
    }
  ],
  "variacoes": [
    {
      "id": 1,
      "tamanho": "P",
      "cor": "Branco",
      "estoque": 10,
      "preco_adicional": 0,
      "disponivel": true
    }
  ],
  "categorias": [
    {"id": 1, "nome": "Bodies", "slug": "bodies"}
  ]
}
```

### POST /produtos
Criar produto (requer autenticação - admin/vendedor)

**Request:**
```json
{
  "codigo": "PROD001",
  "nome": "Nome do Produto",
  "descricao": "Descrição detalhada",
  "genero": "unissex",
  "faixa_etaria": "0-3m",
  "preco_custo": 20.00,
  "preco_venda": 50.00,
  "preco_promocional": 45.00,
  "estoque_atual": 100,
  "estoque_minimo": 10,
  "fornecedor_id": 1,
  "categorias": [1, 2],
  "peso": 0.2,
  "destaque": true
}
```

**Response (201):**
```json
{
  "mensagem": "Produto criado com sucesso",
  "produto": {
    "id": 10,
    "codigo": "PROD001",
    "nome": "Nome do Produto"
  }
}
```

### PUT /produtos/{id}
Atualizar produto (requer autenticação - admin/vendedor)

### DELETE /produtos/{id}
Deletar produto (requer autenticação - admin)

---

## 🛒 Vendas

### POST /vendas
Criar nova venda (requer autenticação)

**Request:**
```json
{
  "cliente_id": 1,
  "origem": "ecommerce",
  "forma_pagamento": "pix",
  "parcelas": 1,
  "desconto": 0,
  "frete": 15.00,
  "status": "pago",
  "itens": [
    {
      "produto_id": 1,
      "variacao_id": 1,
      "quantidade": 2,
      "desconto": 0
    },
    {
      "produto_id": 2,
      "quantidade": 1,
      "desconto": 5.00
    }
  ],
  "observacoes": "Entregar no período da manhã"
}
```

**Response (201):**
```json
{
  "mensagem": "Venda criada com sucesso",
  "venda": {
    "id": 15,
    "numero_venda": "VND202502110001",
    "total": 125.00
  }
}
```

### GET /vendas
Listar vendas (requer autenticação)

**Query Parameters:**
- `status` - pendente, pago, enviado, entregue, cancelado
- `data_inicio` - ISO format (2025-01-01)
- `data_fim` - ISO format
- `cliente_id` - Filtrar por cliente
- `page` - Página
- `per_page` - Itens por página

**Response (200):**
```json
{
  "vendas": [
    {
      "id": 1,
      "numero_venda": "VND202502110001",
      "cliente": "Maria Silva",
      "total": 150.00,
      "status": "pago",
      "origem": "ecommerce",
      "data_venda": "2025-02-11T10:30:00",
      "itens_count": 3
    }
  ],
  "total": 100,
  "paginas": 2,
  "pagina_atual": 1
}
```

### GET /vendas/{id}
Obter detalhes da venda (requer autenticação)

### PATCH /vendas/{id}/status
Atualizar status da venda (requer autenticação)

**Request:**
```json
{
  "status": "enviado"
}
```

---

## 👥 Clientes

### GET /clientes
Listar clientes (requer autenticação)

**Query Parameters:**
- `q` - Busca por nome, email ou CPF
- `page` - Página

### POST /clientes
Criar cliente (requer autenticação)

**Request:**
```json
{
  "nome": "Cliente Teste",
  "cpf": "123.456.789-00",
  "email": "cliente@email.com",
  "telefone": "(11) 99999-9999",
  "cep": "01234-567",
  "logradouro": "Rua Exemplo",
  "numero": "123",
  "bairro": "Centro",
  "cidade": "São Paulo",
  "estado": "SP"
}
```

### GET /clientes/{id}
Obter detalhes do cliente (requer autenticação)

---

## 💰 Financeiro

### GET /financeiro/lancamentos
Listar lançamentos financeiros (requer autenticação)

**Query Parameters:**
- `tipo` - receita, despesa
- `status` - pendente, pago, atrasado, cancelado

**Response (200):**
```json
{
  "lancamentos": [
    {
      "id": 1,
      "tipo": "receita",
      "categoria": "venda",
      "descricao": "Venda VND202502110001",
      "valor": 150.00,
      "status": "pago",
      "data_vencimento": "2025-02-11"
    }
  ]
}
```

### POST /financeiro/lancamentos
Criar lançamento (requer autenticação)

**Request:**
```json
{
  "tipo": "despesa",
  "categoria": "aluguel",
  "descricao": "Aluguel Fevereiro 2025",
  "valor": 2000.00,
  "data_vencimento": "2025-02-05",
  "forma_pagamento": "transferencia"
}
```

### GET /financeiro/fluxo-caixa
Resumo do fluxo de caixa (requer autenticação)

**Response (200):**
```json
{
  "receitas_mes": 15000.00,
  "despesas_mes": 8500.00,
  "saldo_mes": 6500.00,
  "contas_receber": 3000.00,
  "contas_pagar": 2000.00
}
```

---

## 📊 Dashboard / BI

### GET /dashboard/resumo
Métricas gerais do dashboard (requer autenticação)

**Response (200):**
```json
{
  "vendas_mes": 15000.00,
  "vendas_mes_anterior": 12000.00,
  "crescimento_percentual": 25.00,
  "numero_vendas": 45,
  "ticket_medio": 333.33,
  "total_clientes": 120,
  "produtos_ativos": 85,
  "alertas_estoque": 5
}
```

### GET /dashboard/vendas-por-periodo
Vendas agrupadas por período (requer autenticação)

**Query Parameters:**
- `periodo` - dia, semana, mes
- `dias` - Últimos X dias (padrão: 30)

**Response (200):**
```json
{
  "vendas": [
    {
      "data": "2025-02-11",
      "total": 500.00,
      "quantidade": 3
    }
  ]
}
```

### GET /dashboard/produtos-mais-vendidos
Top produtos por quantidade (requer autenticação)

**Query Parameters:**
- `limite` - Número de produtos (padrão: 10)
- `dias` - Período em dias (padrão: 30)

**Response (200):**
```json
{
  "produtos": [
    {
      "id": 1,
      "nome": "Body Manga Longa",
      "quantidade_vendida": 25,
      "receita_total": 875.00
    }
  ]
}
```

### GET /dashboard/vendas-por-categoria
Distribuição de vendas por categoria (requer autenticação)

### GET /dashboard/vendas-por-genero
Distribuição de vendas por gênero (requer autenticação)

### GET /dashboard/taxa-conversao
Taxa de conversão de vendas (requer autenticação)

---

## 📦 Estoque

### GET /estoque/movimentacoes
Listar movimentações de estoque (requer autenticação)

### GET /estoque/alertas
Produtos com estoque baixo (requer autenticação)

**Response (200):**
```json
{
  "alertas": [
    {
      "id": 5,
      "nome": "Vestido Floral",
      "estoque_atual": 3,
      "estoque_minimo": 5
    }
  ]
}
```

---

## ❌ Códigos de Erro

- `400` - Bad Request (dados inválidos)
- `401` - Unauthorized (não autenticado)
- `403` - Forbidden (sem permissão)
- `404` - Not Found (recurso não encontrado)
- `500` - Internal Server Error

**Exemplo de erro:**
```json
{
  "erro": "Email já cadastrado"
}
```
