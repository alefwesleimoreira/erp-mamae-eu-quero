from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Tabela de associação para produtos e categorias (muitos para muitos)
produto_categoria = db.Table('produto_categoria',
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'), primary_key=True),
    db.Column('categoria_id', db.Integer, db.ForeignKey('categoria.id'), primary_key=True)
)

# Tabela de associação para imagens de produtos
class ImagemProduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    principal = db.Column(db.Boolean, default=False)
    ordem = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default='cliente')  # admin, vendedor, cliente
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True)
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date)
    
    # Endereço
    cep = db.Column(db.String(10))
    logradouro = db.Column(db.String(200))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    vendas = db.relationship('Venda', backref='cliente', lazy='dynamic')

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(200), nullable=False)
    nome_fantasia = db.Column(db.String(200))
    cnpj = db.Column(db.String(18), unique=True)
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    
    # Endereço
    cep = db.Column(db.String(10))
    logradouro = db.Column(db.String(200))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    produtos = db.relationship('Produto', backref='fornecedor', lazy='dynamic')

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)
    slug = db.Column(db.String(100), unique=True)
    ativo = db.Column(db.Boolean, default=True)
    ordem = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    slug = db.Column(db.String(200), unique=True)
    
    # Classificação
    genero = db.Column(db.String(20))  # masculino, feminino, unissex
    faixa_etaria = db.Column(db.String(50))  # RN, 0-3m, 3-6m, 6-9m, 1-2a, 2-4a, etc
    
    # Preços
    preco_custo = db.Column(db.Numeric(10, 2), nullable=False)
    preco_venda = db.Column(db.Numeric(10, 2), nullable=False)
    preco_promocional = db.Column(db.Numeric(10, 2))
    margem_lucro = db.Column(db.Numeric(5, 2))
    
    # Estoque
    estoque_atual = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=5)
    estoque_maximo = db.Column(db.Integer, default=100)
    
    # Dimensões e peso
    peso = db.Column(db.Numeric(10, 3))  # em kg
    altura = db.Column(db.Numeric(10, 2))  # em cm
    largura = db.Column(db.Numeric(10, 2))
    profundidade = db.Column(db.Numeric(10, 2))
    
    # Relacionamentos
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))
    categorias = db.relationship('Categoria', secondary=produto_categoria, backref='produtos')
    imagens = db.relationship('ImagemProduto', backref='produto', lazy='dynamic', cascade='all, delete-orphan')
    variacoes = db.relationship('ProdutoVariacao', backref='produto', lazy='dynamic', cascade='all, delete-orphan')
    
    # Controle
    ativo = db.Column(db.Boolean, default=True)
    destaque = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProdutoVariacao(db.Model):
    """Variações do produto (tamanhos, cores)"""
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    tamanho = db.Column(db.String(10))  # P, M, G, GG, 1, 2, 4, 6, 8, etc
    cor = db.Column(db.String(50))
    codigo_sku = db.Column(db.String(50), unique=True)
    estoque = db.Column(db.Integer, default=0)
    preco_adicional = db.Column(db.Numeric(10, 2), default=0)
    ativo = db.Column(db.Boolean, default=True)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_venda = db.Column(db.String(50), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))  # Vendedor
    
    # Valores
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    desconto = db.Column(db.Numeric(10, 2), default=0)
    frete = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Status
    status = db.Column(db.String(20), default='pendente')  # pendente, pago, enviado, entregue, cancelado
    origem = db.Column(db.String(20), default='loja')  # loja, ecommerce
    
    # Pagamento
    forma_pagamento = db.Column(db.String(50))  # dinheiro, cartao_credito, cartao_debito, pix, boleto
    parcelas = db.Column(db.Integer, default=1)
    
    # Datas
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    data_pagamento = db.Column(db.DateTime)
    data_envio = db.Column(db.DateTime)
    data_entrega = db.Column(db.DateTime)
    
    # Observações
    observacoes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    itens = db.relationship('ItemVenda', backref='venda', lazy='dynamic', cascade='all, delete-orphan')

class ItemVenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    variacao_id = db.Column(db.Integer, db.ForeignKey('produto_variacao.id'))
    
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    desconto = db.Column(db.Numeric(10, 2), default=0)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relacionamentos
    produto = db.relationship('Produto')
    variacao = db.relationship('ProdutoVariacao')

class MovimentacaoEstoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    variacao_id = db.Column(db.Integer, db.ForeignKey('produto_variacao.id'))
    
    tipo = db.Column(db.String(20), nullable=False)  # entrada, saida, ajuste, devolucao
    quantidade = db.Column(db.Integer, nullable=False)
    estoque_anterior = db.Column(db.Integer)
    estoque_atual = db.Column(db.Integer)
    
    motivo = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    produto = db.relationship('Produto')

class Financeiro(db.Model):
    """Controle de fluxo de caixa"""
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)  # receita, despesa
    categoria = db.Column(db.String(50), nullable=False)  # venda, compra, aluguel, salario, etc
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relacionamentos opcionais
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'))
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))
    
    # Datas
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date)
    
    # Status
    status = db.Column(db.String(20), default='pendente')  # pendente, pago, atrasado, cancelado
    
    forma_pagamento = db.Column(db.String(50))
    observacoes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
