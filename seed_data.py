"""
Script para popular o banco de dados com dados de exemplo
Execute: python seed_data.py
"""
from app import create_app, db
from app.models import (
    Usuario, Cliente, Fornecedor, Categoria, Produto, 
    ProdutoVariacao, ImagemProduto, Venda, ItemVenda, Financeiro
)
from datetime import datetime, timedelta
import random

app = create_app()

def seed_database():
    with app.app_context():
        print("🗑️  Limpando banco de dados...")
        db.drop_all()
        db.create_all()
        
        print("👤 Criando usuários...")
        # Admin
        admin = Usuario(nome="Administrador", email="admin@loja.com", tipo="admin", ativo=True)
        admin.set_senha("admin123")
        db.session.add(admin)
        
        # Vendedor
        vendedor = Usuario(nome="Vendedor", email="vendedor@loja.com", tipo="vendedor", ativo=True)
        vendedor.set_senha("vendedor123")
        db.session.add(vendedor)
        
        db.session.commit()
        
        print("🏢 Criando fornecedores...")
        fornecedores = [
            Fornecedor(
                razao_social="Confecções Baby Ltda",
                nome_fantasia="Baby Fashion",
                cnpj="12.345.678/0001-90",
                email="contato@babyfashion.com",
                telefone="(11) 98765-4321",
                cidade="São Paulo",
                estado="SP"
            ),
            Fornecedor(
                razao_social="Textil Infantil SA",
                nome_fantasia="Kids Wear",
                cnpj="98.765.432/0001-10",
                email="vendas@kidswear.com",
                telefone="(11) 91234-5678",
                cidade="São Paulo",
                estado="SP"
            )
        ]
        for f in fornecedores:
            db.session.add(f)
        db.session.commit()
        
        print("📂 Criando categorias...")
        categorias = [
            Categoria(nome="Bodies", slug="bodies", ordem=1),
            Categoria(nome="Macacões", slug="macacoes", ordem=2),
            Categoria(nome="Conjuntos", slug="conjuntos", ordem=3),
            Categoria(nome="Calças", slug="calcas", ordem=4),
            Categoria(nome="Vestidos", slug="vestidos", ordem=5),
            Categoria(nome="Pijamas", slug="pijamas", ordem=6),
        ]
        for c in categorias:
            db.session.add(c)
        db.session.commit()
        
        print("👕 Criando produtos...")
        produtos_data = [
            {
                "codigo": "BODY001",
                "nome": "Body Manga Longa Listrado",
                "descricao": "Body confortável em algodão, perfeito para o dia a dia",
                "genero": "unissex",
                "faixa_etaria": "0-3m",
                "preco_custo": 15.00,
                "preco_venda": 35.00,
                "estoque_atual": 50,
                "categorias": [0],  # Bodies
                "tamanhos": ["RN", "P", "M", "G"],
                "cores": ["Branco", "Azul", "Rosa"]
            },
            {
                "codigo": "MAC001",
                "nome": "Macacão de Plush",
                "descricao": "Macacão macio e quentinho para bebês",
                "genero": "unissex",
                "faixa_etaria": "3-6m",
                "preco_custo": 30.00,
                "preco_venda": 75.00,
                "preco_promocional": 65.00,
                "estoque_atual": 30,
                "categorias": [1],  # Macacões
                "tamanhos": ["P", "M", "G"],
                "cores": ["Azul", "Rosa", "Amarelo"]
            },
            {
                "codigo": "CONJ001",
                "nome": "Conjunto Calça e Blusa Dinossauro",
                "descricao": "Conjunto estampado super divertido",
                "genero": "masculino",
                "faixa_etaria": "1-2a",
                "preco_custo": 25.00,
                "preco_venda": 60.00,
                "estoque_atual": 40,
                "categorias": [2],  # Conjuntos
                "tamanhos": ["1", "2"],
                "cores": ["Verde", "Azul"]
            },
            {
                "codigo": "VEST001",
                "nome": "Vestido Floral",
                "descricao": "Lindo vestido com estampa de flores",
                "genero": "feminino",
                "faixa_etaria": "2-4a",
                "preco_custo": 28.00,
                "preco_venda": 70.00,
                "estoque_atual": 25,
                "destaque": True,
                "categorias": [4],  # Vestidos
                "tamanhos": ["2", "4"],
                "cores": ["Rosa", "Lilás", "Branco"]
            },
            {
                "codigo": "PJ001",
                "nome": "Pijama de Unicórnio",
                "descricao": "Pijama super fofo e confortável",
                "genero": "feminino",
                "faixa_etaria": "3-4a",
                "preco_custo": 22.00,
                "preco_venda": 55.00,
                "estoque_atual": 35,
                "destaque": True,
                "categorias": [5],  # Pijamas
                "tamanhos": ["3", "4"],
                "cores": ["Rosa", "Roxo"]
            },
            {
                "codigo": "CALC001",
                "nome": "Calça Jeans Infantil",
                "descricao": "Calça jeans resistente e confortável",
                "genero": "unissex",
                "faixa_etaria": "2-4a",
                "preco_custo": 35.00,
                "preco_venda": 85.00,
                "estoque_atual": 20,
                "categorias": [3],  # Calças
                "tamanhos": ["2", "4", "6"],
                "cores": ["Azul", "Preto"]
            }
        ]
        
        for p_data in produtos_data:
            produto = Produto(
                codigo=p_data["codigo"],
                nome=p_data["nome"],
                descricao=p_data["descricao"],
                slug=p_data["nome"].lower().replace(" ", "-"),
                genero=p_data["genero"],
                faixa_etaria=p_data["faixa_etaria"],
                preco_custo=p_data["preco_custo"],
                preco_venda=p_data["preco_venda"],
                preco_promocional=p_data.get("preco_promocional"),
                estoque_atual=p_data["estoque_atual"],
                fornecedor=fornecedores[0],
                destaque=p_data.get("destaque", False)
            )
            
            # Adicionar categorias
            for cat_idx in p_data["categorias"]:
                produto.categorias.append(categorias[cat_idx])
            
            db.session.add(produto)
            db.session.flush()
            
            # Criar variações
            for tamanho in p_data["tamanhos"]:
                for cor in p_data["cores"]:
                    variacao = ProdutoVariacao(
                        produto_id=produto.id,
                        tamanho=tamanho,
                        cor=cor,
                        codigo_sku=f"{p_data['codigo']}-{tamanho}-{cor[:3].upper()}",
                        estoque=random.randint(5, 15)
                    )
                    db.session.add(variacao)
        
        db.session.commit()
        
        print("👥 Criando clientes...")
        clientes = [
            Cliente(
                nome="Maria Silva",
                email="maria@email.com",
                cpf="123.456.789-00",
                telefone="(11) 98888-7777",
                cidade="São Paulo",
                estado="SP"
            ),
            Cliente(
                nome="João Santos",
                email="joao@email.com",
                cpf="987.654.321-00",
                telefone="(11) 97777-8888",
                cidade="São Paulo",
                estado="SP"
            ),
            Cliente(
                nome="Ana Oliveira",
                email="ana@email.com",
                cpf="456.789.123-00",
                telefone="(11) 96666-9999",
                cidade="Campinas",
                estado="SP"
            )
        ]
        for c in clientes:
            db.session.add(c)
        db.session.commit()
        
        print("💰 Criando vendas de exemplo...")
        produtos = Produto.query.all()
        
        for i in range(10):
            data_venda = datetime.now() - timedelta(days=random.randint(0, 30))
            
            venda = Venda(
                numero_venda=f"VND2025{random.randint(1000, 9999)}",
                cliente=random.choice(clientes),
                usuario=admin,
                data_venda=data_venda,
                origem="ecommerce" if i % 2 == 0 else "loja",
                forma_pagamento=random.choice(["pix", "cartao_credito", "dinheiro"]),
                status=random.choice(["pago", "enviado", "entregue"])
            )
            
            subtotal = 0
            num_itens = random.randint(1, 3)
            
            for _ in range(num_itens):
                produto = random.choice(produtos)
                quantidade = random.randint(1, 3)
                preco = produto.preco_promocional or produto.preco_venda
                
                item = ItemVenda(
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=preco,
                    subtotal=preco * quantidade
                )
                venda.itens.append(item)
                subtotal += item.subtotal
            
            venda.subtotal = subtotal
            venda.total = subtotal
            venda.data_pagamento = data_venda
            
            db.session.add(venda)
            
            # Adicionar ao financeiro
            financeiro = Financeiro(
                tipo="receita",
                categoria="venda",
                descricao=f"Venda {venda.numero_venda}",
                valor=venda.total,
                venda=venda,
                data_vencimento=data_venda.date(),
                data_pagamento=data_venda.date(),
                status="pago",
                forma_pagamento=venda.forma_pagamento
            )
            db.session.add(financeiro)
        
        # Adicionar algumas despesas
        print("💸 Criando despesas de exemplo...")
        despesas = [
            ("Aluguel", 2000.00, "aluguel"),
            ("Luz", 350.00, "utilidades"),
            ("Internet", 120.00, "utilidades"),
            ("Salários", 5000.00, "salario"),
        ]
        
        for desc, valor, categoria in despesas:
            financeiro = Financeiro(
                tipo="despesa",
                categoria=categoria,
                descricao=desc,
                valor=valor,
                data_vencimento=(datetime.now() - timedelta(days=5)).date(),
                data_pagamento=(datetime.now() - timedelta(days=5)).date(),
                status="pago",
                forma_pagamento="transferencia"
            )
            db.session.add(financeiro)
        
        db.session.commit()
        
        print("✅ Banco de dados populado com sucesso!")
        print("\n📊 Resumo:")
        print(f"   - {Usuario.query.count()} usuários")
        print(f"   - {Fornecedor.query.count()} fornecedores")
        print(f"   - {Categoria.query.count()} categorias")
        print(f"   - {Produto.query.count()} produtos")
        print(f"   - {Cliente.query.count()} clientes")
        print(f"   - {Venda.query.count()} vendas")
        print(f"   - {Financeiro.query.count()} lançamentos financeiros")
        print("\n🔑 Credenciais de acesso:")
        print("   Admin: admin@loja.com / admin123")
        print("   Vendedor: vendedor@loja.com / vendedor123")

if __name__ == "__main__":
    seed_database()
