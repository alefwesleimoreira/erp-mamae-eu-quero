from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Produto, Categoria, ProdutoVariacao, ImagemProduto, Usuario
from sqlalchemy import or_, and_

bp = Blueprint('produtos', __name__, url_prefix='/api/produtos')

@bp.route('/', methods=['GET'])
def listar_produtos():
    """Listar produtos (público para e-commerce)"""
    # Filtros
    categoria_id = request.args.get('categoria_id', type=int)
    genero = request.args.get('genero')
    faixa_etaria = request.args.get('faixa_etaria')
    busca = request.args.get('q')
    destaque = request.args.get('destaque', type=bool)
    ordem = request.args.get('ordem', 'recentes')  # recentes, preco_asc, preco_desc, nome
    
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Query base
    query = Produto.query.filter_by(ativo=True)
    
    # Aplicar filtros
    if categoria_id:
        query = query.filter(Produto.categorias.any(id=categoria_id))
    
    if genero:
        query = query.filter_by(genero=genero)
    
    if faixa_etaria:
        query = query.filter_by(faixa_etaria=faixa_etaria)
    
    if destaque:
        query = query.filter_by(destaque=True)
    
    if busca:
        query = query.filter(
            or_(
                Produto.nome.ilike(f'%{busca}%'),
                Produto.descricao.ilike(f'%{busca}%'),
                Produto.codigo.ilike(f'%{busca}%')
            )
        )
    
    # Ordenação
    if ordem == 'preco_asc':
        query = query.order_by(Produto.preco_venda.asc())
    elif ordem == 'preco_desc':
        query = query.order_by(Produto.preco_venda.desc())
    elif ordem == 'nome':
        query = query.order_by(Produto.nome.asc())
    else:  # recentes
        query = query.order_by(Produto.created_at.desc())
    
    # Paginação
    produtos_paginados = query.paginate(page=page, per_page=per_page, error_out=False)
    
    produtos_lista = []
    for produto in produtos_paginados.items:
        imagem_principal = produto.imagens.filter_by(principal=True).first()
        if not imagem_principal:
            imagem_principal = produto.imagens.first()
        
        produtos_lista.append({
            'id': produto.id,
            'codigo': produto.codigo,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'slug': produto.slug,
            'preco_venda': float(produto.preco_venda),
            'preco_promocional': float(produto.preco_promocional) if produto.preco_promocional else None,
            'estoque_disponivel': produto.estoque_atual > 0,
            'destaque': produto.destaque,
            'genero': produto.genero,
            'faixa_etaria': produto.faixa_etaria,
            'imagem': imagem_principal.url if imagem_principal else None,
            'categorias': [{'id': cat.id, 'nome': cat.nome} for cat in produto.categorias]
        })
    
    return jsonify({
        'produtos': produtos_lista,
        'total': produtos_paginados.total,
        'paginas': produtos_paginados.pages,
        'pagina_atual': page,
        'por_pagina': per_page
    }), 200

@bp.route('/<int:id>', methods=['GET'])
def obter_produto(id):
    """Obter detalhes de um produto"""
    produto = Produto.query.get(id)
    
    if not produto or not produto.ativo:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    # Buscar todas as imagens
    imagens = [{
        'id': img.id,
        'url': img.url,
        'principal': img.principal,
        'ordem': img.ordem
    } for img in produto.imagens.order_by(ImagemProduto.ordem).all()]
    
    # Buscar variações
    variacoes = [{
        'id': var.id,
        'tamanho': var.tamanho,
        'cor': var.cor,
        'estoque': var.estoque,
        'preco_adicional': float(var.preco_adicional),
        'disponivel': var.estoque > 0 and var.ativo
    } for var in produto.variacoes.filter_by(ativo=True).all()]
    
    return jsonify({
        'id': produto.id,
        'codigo': produto.codigo,
        'nome': produto.nome,
        'descricao': produto.descricao,
        'slug': produto.slug,
        'genero': produto.genero,
        'faixa_etaria': produto.faixa_etaria,
        'preco_venda': float(produto.preco_venda),
        'preco_promocional': float(produto.preco_promocional) if produto.preco_promocional else None,
        'estoque_atual': produto.estoque_atual,
        'peso': float(produto.peso) if produto.peso else None,
        'dimensoes': {
            'altura': float(produto.altura) if produto.altura else None,
            'largura': float(produto.largura) if produto.largura else None,
            'profundidade': float(produto.profundidade) if produto.profundidade else None
        },
        'imagens': imagens,
        'variacoes': variacoes,
        'categorias': [{'id': cat.id, 'nome': cat.nome, 'slug': cat.slug} for cat in produto.categorias]
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def criar_produto():
    """Criar novo produto (apenas admin/vendedor)"""
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    
    if usuario.tipo not in ['admin', 'vendedor']:
        return jsonify({'erro': 'Acesso negado'}), 403
    
    data = request.get_json()
    
    # Validações
    if not data.get('codigo') or not data.get('nome'):
        return jsonify({'erro': 'Código e nome são obrigatórios'}), 400
    
    if Produto.query.filter_by(codigo=data['codigo']).first():
        return jsonify({'erro': 'Código já existe'}), 400
    
    # Criar produto
    produto = Produto(
        codigo=data['codigo'],
        nome=data['nome'],
        descricao=data.get('descricao'),
        slug=data.get('slug') or data['nome'].lower().replace(' ', '-'),
        genero=data.get('genero'),
        faixa_etaria=data.get('faixa_etaria'),
        preco_custo=data.get('preco_custo', 0),
        preco_venda=data.get('preco_venda', 0),
        preco_promocional=data.get('preco_promocional'),
        estoque_atual=data.get('estoque_atual', 0),
        estoque_minimo=data.get('estoque_minimo', 5),
        estoque_maximo=data.get('estoque_maximo', 100),
        fornecedor_id=data.get('fornecedor_id'),
        peso=data.get('peso'),
        altura=data.get('altura'),
        largura=data.get('largura'),
        profundidade=data.get('profundidade'),
        ativo=data.get('ativo', True),
        destaque=data.get('destaque', False)
    )
    
    # Calcular margem de lucro
    if produto.preco_custo and produto.preco_venda:
        produto.margem_lucro = ((produto.preco_venda - produto.preco_custo) / produto.preco_custo) * 100
    
    # Adicionar categorias
    if data.get('categorias'):
        categorias = Categoria.query.filter(Categoria.id.in_(data['categorias'])).all()
        produto.categorias = categorias
    
    db.session.add(produto)
    db.session.commit()
    
    return jsonify({
        'mensagem': 'Produto criado com sucesso',
        'produto': {
            'id': produto.id,
            'codigo': produto.codigo,
            'nome': produto.nome
        }
    }), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_produto(id):
    """Atualizar produto (apenas admin/vendedor)"""
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    
    if usuario.tipo not in ['admin', 'vendedor']:
        return jsonify({'erro': 'Acesso negado'}), 403
    
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    data = request.get_json()
    
    # Atualizar campos
    campos_atualizaveis = [
        'nome', 'descricao', 'slug', 'genero', 'faixa_etaria',
        'preco_custo', 'preco_venda', 'preco_promocional',
        'estoque_atual', 'estoque_minimo', 'estoque_maximo',
        'fornecedor_id', 'peso', 'altura', 'largura', 'profundidade',
        'ativo', 'destaque'
    ]
    
    for campo in campos_atualizaveis:
        if campo in data:
            setattr(produto, campo, data[campo])
    
    # Recalcular margem de lucro
    if produto.preco_custo and produto.preco_venda:
        produto.margem_lucro = ((produto.preco_venda - produto.preco_custo) / produto.preco_custo) * 100
    
    # Atualizar categorias
    if 'categorias' in data:
        categorias = Categoria.query.filter(Categoria.id.in_(data['categorias'])).all()
        produto.categorias = categorias
    
    db.session.commit()
    
    return jsonify({'mensagem': 'Produto atualizado com sucesso'}), 200

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_produto(id):
    """Deletar produto (apenas admin)"""
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    
    if usuario.tipo != 'admin':
        return jsonify({'erro': 'Acesso negado'}), 403
    
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    # Soft delete
    produto.ativo = False
    db.session.commit()
    
    return jsonify({'mensagem': 'Produto deletado com sucesso'}), 200

# Rotas de categorias
@bp.route('/categorias', methods=['GET'])
def listar_categorias():
    """Listar categorias"""
    categorias = Categoria.query.filter_by(ativo=True).order_by(Categoria.ordem, Categoria.nome).all()
    
    return jsonify({
        'categorias': [{
            'id': cat.id,
            'nome': cat.nome,
            'descricao': cat.descricao,
            'slug': cat.slug
        } for cat in categorias]
    }), 200

@bp.route('/categorias', methods=['POST'])
@jwt_required()
def criar_categoria():
    """Criar categoria (apenas admin)"""
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    
    if usuario.tipo != 'admin':
        return jsonify({'erro': 'Acesso negado'}), 403
    
    data = request.get_json()
    
    if not data.get('nome'):
        return jsonify({'erro': 'Nome é obrigatório'}), 400
    
    categoria = Categoria(
        nome=data['nome'],
        descricao=data.get('descricao'),
        slug=data.get('slug') or data['nome'].lower().replace(' ', '-'),
        ordem=data.get('ordem', 0)
    )
    
    db.session.add(categoria)
    db.session.commit()
    
    return jsonify({
        'mensagem': 'Categoria criada com sucesso',
        'categoria': {'id': categoria.id, 'nome': categoria.nome}
    }), 201
