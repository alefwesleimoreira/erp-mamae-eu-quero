from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Venda, ItemVenda, Produto, Cliente, MovimentacaoEstoque, Financeiro, ProdutoVariacao
from datetime import datetime
import random
import string

bp = Blueprint('vendas', __name__, url_prefix='/api/vendas')

def gerar_numero_venda():
    """Gerar número único de venda"""
    hoje = datetime.now().strftime('%Y%m%d')
    aleatorio = ''.join(random.choices(string.digits, k=4))
    return f'VND{hoje}{aleatorio}'

@bp.route('/', methods=['POST'])
@jwt_required()
def criar_venda():
    """Criar nova venda"""
    usuario_id = get_jwt_identity()
    data = request.get_json()
    
    # Validações
    if not data.get('cliente_id') or not data.get('itens'):
        return jsonify({'erro': 'Cliente e itens são obrigatórios'}), 400
    
    cliente = Cliente.query.get(data['cliente_id'])
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404
    
    # Criar venda
    venda = Venda(
        numero_venda=gerar_numero_venda(),
        cliente_id=data['cliente_id'],
        usuario_id=usuario_id,
        origem=data.get('origem', 'loja'),
        forma_pagamento=data.get('forma_pagamento'),
        parcelas=data.get('parcelas', 1),
        desconto=data.get('desconto', 0),
        frete=data.get('frete', 0),
        observacoes=data.get('observacoes')
    )
    
    subtotal = 0
    
    # Adicionar itens
    for item_data in data['itens']:
        produto = Produto.query.get(item_data['produto_id'])
        if not produto:
            return jsonify({'erro': f'Produto {item_data["produto_id"]} não encontrado'}), 404
        
        # Verificar estoque
        estoque_disponivel = produto.estoque_atual
        variacao = None
        
        if item_data.get('variacao_id'):
            variacao = ProdutoVariacao.query.get(item_data['variacao_id'])
            if variacao:
                estoque_disponivel = variacao.estoque
        
        if estoque_disponivel < item_data['quantidade']:
            return jsonify({'erro': f'Estoque insuficiente para {produto.nome}'}), 400
        
        # Calcular preço
        preco_unitario = produto.preco_promocional or produto.preco_venda
        if variacao and variacao.preco_adicional:
            preco_unitario += variacao.preco_adicional
        
        item_subtotal = (preco_unitario * item_data['quantidade']) - item_data.get('desconto', 0)
        
        item_venda = ItemVenda(
            produto_id=produto.id,
            variacao_id=item_data.get('variacao_id'),
            quantidade=item_data['quantidade'],
            preco_unitario=preco_unitario,
            desconto=item_data.get('desconto', 0),
            subtotal=item_subtotal
        )
        
        venda.itens.append(item_venda)
        subtotal += item_subtotal
        
        # Baixar estoque
        estoque_anterior = estoque_disponivel
        if variacao:
            variacao.estoque -= item_data['quantidade']
            estoque_atual = variacao.estoque
        else:
            produto.estoque_atual -= item_data['quantidade']
            estoque_atual = produto.estoque_atual
        
        # Registrar movimentação
        movimentacao = MovimentacaoEstoque(
            produto_id=produto.id,
            variacao_id=variacao.id if variacao else None,
            tipo='saida',
            quantidade=item_data['quantidade'],
            estoque_anterior=estoque_anterior,
            estoque_atual=estoque_atual,
            motivo='Venda',
            usuario_id=usuario_id
        )
        db.session.add(movimentacao)
    
    venda.subtotal = subtotal
    venda.total = subtotal - venda.desconto + venda.frete
    
    # Se pago, registrar no financeiro
    if data.get('status') == 'pago':
        venda.status = 'pago'
        venda.data_pagamento = datetime.utcnow()
        
        financeiro = Financeiro(
            tipo='receita',
            categoria='venda',
            descricao=f'Venda {venda.numero_venda}',
            valor=venda.total,
            venda_id=venda.id,
            data_vencimento=datetime.utcnow().date(),
            data_pagamento=datetime.utcnow().date(),
            status='pago',
            forma_pagamento=venda.forma_pagamento
        )
        db.session.add(financeiro)
    
    db.session.add(venda)
    db.session.commit()
    
    return jsonify({
        'mensagem': 'Venda criada com sucesso',
        'venda': {
            'id': venda.id,
            'numero_venda': venda.numero_venda,
            'total': float(venda.total)
        }
    }), 201

@bp.route('/', methods=['GET'])
@jwt_required()
def listar_vendas():
    """Listar vendas"""
    # Filtros
    status = request.args.get('status')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    cliente_id = request.args.get('cliente_id', type=int)
    
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    query = Venda.query
    
    if status:
        query = query.filter_by(status=status)
    
    if cliente_id:
        query = query.filter_by(cliente_id=cliente_id)
    
    if data_inicio:
        query = query.filter(Venda.data_venda >= datetime.fromisoformat(data_inicio))
    
    if data_fim:
        query = query.filter(Venda.data_venda <= datetime.fromisoformat(data_fim))
    
    query = query.order_by(Venda.data_venda.desc())
    vendas_paginadas = query.paginate(page=page, per_page=per_page, error_out=False)
    
    vendas_lista = []
    for venda in vendas_paginadas.items:
        vendas_lista.append({
            'id': venda.id,
            'numero_venda': venda.numero_venda,
            'cliente': venda.cliente.nome,
            'total': float(venda.total),
            'status': venda.status,
            'origem': venda.origem,
            'data_venda': venda.data_venda.isoformat(),
            'itens_count': venda.itens.count()
        })
    
    return jsonify({
        'vendas': vendas_lista,
        'total': vendas_paginadas.total,
        'paginas': vendas_paginadas.pages,
        'pagina_atual': page
    }), 200

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_venda(id):
    """Obter detalhes de uma venda"""
    venda = Venda.query.get(id)
    
    if not venda:
        return jsonify({'erro': 'Venda não encontrada'}), 404
    
    itens = []
    for item in venda.itens:
        itens.append({
            'id': item.id,
            'produto': item.produto.nome,
            'quantidade': item.quantidade,
            'preco_unitario': float(item.preco_unitario),
            'desconto': float(item.desconto),
            'subtotal': float(item.subtotal)
        })
    
    return jsonify({
        'id': venda.id,
        'numero_venda': venda.numero_venda,
        'cliente': {
            'id': venda.cliente.id,
            'nome': venda.cliente.nome,
            'email': venda.cliente.email
        },
        'subtotal': float(venda.subtotal),
        'desconto': float(venda.desconto),
        'frete': float(venda.frete),
        'total': float(venda.total),
        'status': venda.status,
        'origem': venda.origem,
        'forma_pagamento': venda.forma_pagamento,
        'parcelas': venda.parcelas,
        'data_venda': venda.data_venda.isoformat(),
        'itens': itens,
        'observacoes': venda.observacoes
    }), 200

@bp.route('/<int:id>/status', methods=['PATCH'])
@jwt_required()
def atualizar_status(id):
    """Atualizar status da venda"""
    venda = Venda.query.get(id)
    
    if not venda:
        return jsonify({'erro': 'Venda não encontrada'}), 404
    
    data = request.get_json()
    novo_status = data.get('status')
    
    if novo_status not in ['pendente', 'pago', 'enviado', 'entregue', 'cancelado']:
        return jsonify({'erro': 'Status inválido'}), 400
    
    venda.status = novo_status
    
    # Atualizar datas
    if novo_status == 'pago' and not venda.data_pagamento:
        venda.data_pagamento = datetime.utcnow()
    elif novo_status == 'enviado' and not venda.data_envio:
        venda.data_envio = datetime.utcnow()
    elif novo_status == 'entregue' and not venda.data_entrega:
        venda.data_entrega = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'mensagem': 'Status atualizado com sucesso'}), 200
