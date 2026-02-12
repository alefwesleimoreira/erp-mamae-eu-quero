from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Venda, Produto, Cliente, Financeiro, ItemVenda
from sqlalchemy import func, extract
from datetime import datetime, timedelta

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('/resumo', methods=['GET'])
@jwt_required()
def resumo_geral():
    """Dashboard principal com métricas gerais"""
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1)
    mes_passado = (inicio_mes - timedelta(days=1)).replace(day=1)
    
    # Vendas do mês
    vendas_mes = db.session.query(func.sum(Venda.total)).filter(
        Venda.data_venda >= inicio_mes,
        Venda.status != 'cancelado'
    ).scalar() or 0
    
    # Vendas mês anterior
    vendas_mes_anterior = db.session.query(func.sum(Venda.total)).filter(
        Venda.data_venda >= mes_passado,
        Venda.data_venda < inicio_mes,
        Venda.status != 'cancelado'
    ).scalar() or 0
    
    # Crescimento
    crescimento = 0
    if vendas_mes_anterior > 0:
        crescimento = ((vendas_mes - vendas_mes_anterior) / vendas_mes_anterior) * 100
    
    # Número de vendas
    num_vendas = Venda.query.filter(
        Venda.data_venda >= inicio_mes,
        Venda.status != 'cancelado'
    ).count()
    
    # Ticket médio
    ticket_medio = vendas_mes / num_vendas if num_vendas > 0 else 0
    
    # Total de clientes
    total_clientes = Cliente.query.count()
    
    # Produtos ativos
    produtos_ativos = Produto.query.filter_by(ativo=True).count()
    
    # Produtos com estoque baixo
    produtos_estoque_baixo = Produto.query.filter(
        Produto.estoque_atual <= Produto.estoque_minimo,
        Produto.ativo == True
    ).count()
    
    return jsonify({
        'vendas_mes': float(vendas_mes),
        'vendas_mes_anterior': float(vendas_mes_anterior),
        'crescimento_percentual': round(crescimento, 2),
        'numero_vendas': num_vendas,
        'ticket_medio': float(ticket_medio),
        'total_clientes': total_clientes,
        'produtos_ativos': produtos_ativos,
        'alertas_estoque': produtos_estoque_baixo
    }), 200

@bp.route('/vendas-por-periodo', methods=['GET'])
@jwt_required()
def vendas_por_periodo():
    """Vendas agrupadas por dia/semana/mês"""
    periodo = request.args.get('periodo', 'dia')  # dia, semana, mes
    dias = request.args.get('dias', 30, type=int)
    
    data_inicio = datetime.now() - timedelta(days=dias)
    
    if periodo == 'dia':
        vendas = db.session.query(
            func.date(Venda.data_venda).label('data'),
            func.sum(Venda.total).label('total'),
            func.count(Venda.id).label('quantidade')
        ).filter(
            Venda.data_venda >= data_inicio,
            Venda.status != 'cancelado'
        ).group_by(func.date(Venda.data_venda)).all()
        
        return jsonify({
            'vendas': [{
                'data': v.data.isoformat(),
                'total': float(v.total),
                'quantidade': v.quantidade
            } for v in vendas]
        }), 200
    
    elif periodo == 'mes':
        vendas = db.session.query(
            extract('year', Venda.data_venda).label('ano'),
            extract('month', Venda.data_venda).label('mes'),
            func.sum(Venda.total).label('total'),
            func.count(Venda.id).label('quantidade')
        ).filter(
            Venda.status != 'cancelado'
        ).group_by('ano', 'mes').order_by('ano', 'mes').limit(12).all()
        
        return jsonify({
            'vendas': [{
                'mes': f'{int(v.ano)}-{int(v.mes):02d}',
                'total': float(v.total),
                'quantidade': v.quantidade
            } for v in vendas]
        }), 200

@bp.route('/produtos-mais-vendidos', methods=['GET'])
@jwt_required()
def produtos_mais_vendidos():
    """Top produtos por quantidade vendida"""
    limite = request.args.get('limite', 10, type=int)
    dias = request.args.get('dias', 30, type=int)
    
    data_inicio = datetime.now() - timedelta(days=dias)
    
    produtos = db.session.query(
        Produto.id,
        Produto.nome,
        func.sum(ItemVenda.quantidade).label('quantidade_vendida'),
        func.sum(ItemVenda.subtotal).label('receita_total')
    ).join(
        ItemVenda, ItemVenda.produto_id == Produto.id
    ).join(
        Venda, Venda.id == ItemVenda.venda_id
    ).filter(
        Venda.data_venda >= data_inicio,
        Venda.status != 'cancelado'
    ).group_by(
        Produto.id, Produto.nome
    ).order_by(
        func.sum(ItemVenda.quantidade).desc()
    ).limit(limite).all()
    
    return jsonify({
        'produtos': [{
            'id': p.id,
            'nome': p.nome,
            'quantidade_vendida': p.quantidade_vendida,
            'receita_total': float(p.receita_total)
        } for p in produtos]
    }), 200

@bp.route('/vendas-por-categoria', methods=['GET'])
@jwt_required()
def vendas_por_categoria():
    """Distribuição de vendas por categoria"""
    dias = request.args.get('dias', 30, type=int)
    data_inicio = datetime.now() - timedelta(days=dias)
    
    # Query complexa - produtos podem ter múltiplas categorias
    from app.models import Categoria, produto_categoria
    
    categorias = db.session.query(
        Categoria.nome,
        func.sum(ItemVenda.subtotal).label('total')
    ).join(
        produto_categoria, produto_categoria.c.categoria_id == Categoria.id
    ).join(
        Produto, Produto.id == produto_categoria.c.produto_id
    ).join(
        ItemVenda, ItemVenda.produto_id == Produto.id
    ).join(
        Venda, Venda.id == ItemVenda.venda_id
    ).filter(
        Venda.data_venda >= data_inicio,
        Venda.status != 'cancelado'
    ).group_by(Categoria.nome).all()
    
    return jsonify({
        'categorias': [{
            'nome': c.nome,
            'total': float(c.total)
        } for c in categorias]
    }), 200

@bp.route('/vendas-por-genero', methods=['GET'])
@jwt_required()
def vendas_por_genero():
    """Distribuição de vendas por gênero"""
    dias = request.args.get('dias', 30, type=int)
    data_inicio = datetime.now() - timedelta(days=dias)
    
    generos = db.session.query(
        Produto.genero,
        func.sum(ItemVenda.quantidade).label('quantidade'),
        func.sum(ItemVenda.subtotal).label('total')
    ).join(
        ItemVenda, ItemVenda.produto_id == Produto.id
    ).join(
        Venda, Venda.id == ItemVenda.venda_id
    ).filter(
        Venda.data_venda >= data_inicio,
        Venda.status != 'cancelado',
        Produto.genero.isnot(None)
    ).group_by(Produto.genero).all()
    
    return jsonify({
        'generos': [{
            'genero': g.genero,
            'quantidade': g.quantidade,
            'total': float(g.total)
        } for g in generos]
    }), 200

@bp.route('/taxa-conversao', methods=['GET'])
@jwt_required()
def taxa_conversao():
    """Taxa de conversão e métricas de vendas"""
    dias = request.args.get('dias', 30, type=int)
    data_inicio = datetime.now() - timedelta(days=dias)
    
    # Vendas finalizadas
    vendas_finalizadas = Venda.query.filter(
        Venda.data_venda >= data_inicio,
        Venda.status.in_(['pago', 'enviado', 'entregue'])
    ).count()
    
    # Vendas canceladas
    vendas_canceladas = Venda.query.filter(
        Venda.data_venda >= data_inicio,
        Venda.status == 'cancelado'
    ).count()
    
    # Vendas pendentes
    vendas_pendentes = Venda.query.filter(
        Venda.data_venda >= data_inicio,
        Venda.status == 'pendente'
    ).count()
    
    total_vendas = vendas_finalizadas + vendas_canceladas + vendas_pendentes
    taxa = (vendas_finalizadas / total_vendas * 100) if total_vendas > 0 else 0
    
    return jsonify({
        'vendas_finalizadas': vendas_finalizadas,
        'vendas_canceladas': vendas_canceladas,
        'vendas_pendentes': vendas_pendentes,
        'taxa_conversao': round(taxa, 2)
    }), 200
