# estoque.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Produto, MovimentacaoEstoque

bp = Blueprint('estoque', __name__, url_prefix='/api/estoque')

@bp.route('/movimentacoes', methods=['GET'])
@jwt_required()
def listar_movimentacoes():
    page = request.args.get('page', 1, type=int)
    movimentacoes = MovimentacaoEstoque.query.order_by(
        MovimentacaoEstoque.data_movimentacao.desc()
    ).paginate(page=page, per_page=50, error_out=False)
    
    return jsonify({
        'movimentacoes': [{
            'id': m.id,
            'produto': m.produto.nome,
            'tipo': m.tipo,
            'quantidade': m.quantidade,
            'estoque_atual': m.estoque_atual,
            'data': m.data_movimentacao.isoformat()
        } for m in movimentacoes.items],
        'total': movimentacoes.total
    }), 200

@bp.route('/alertas', methods=['GET'])
@jwt_required()
def alertas_estoque():
    """Produtos com estoque baixo"""
    produtos = Produto.query.filter(
        Produto.estoque_atual <= Produto.estoque_minimo,
        Produto.ativo == True
    ).all()
    
    return jsonify({
        'alertas': [{
            'id': p.id,
            'nome': p.nome,
            'estoque_atual': p.estoque_atual,
            'estoque_minimo': p.estoque_minimo
        } for p in produtos]
    }), 200
