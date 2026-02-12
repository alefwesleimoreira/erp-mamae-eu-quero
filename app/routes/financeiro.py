from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Financeiro
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('financeiro', __name__, url_prefix='/api/financeiro')

@bp.route('/lancamentos', methods=['GET'])
@jwt_required()
def listar_lancamentos():
    tipo = request.args.get('tipo')
    status = request.args.get('status')
    
    query = Financeiro.query
    if tipo:
        query = query.filter_by(tipo=tipo)
    if status:
        query = query.filter_by(status=status)
    
    lancamentos = query.order_by(Financeiro.data_vencimento.desc()).limit(100).all()
    
    return jsonify({
        'lancamentos': [{
            'id': l.id,
            'tipo': l.tipo,
            'categoria': l.categoria,
            'descricao': l.descricao,
            'valor': float(l.valor),
            'status': l.status,
            'data_vencimento': l.data_vencimento.isoformat()
        } for l in lancamentos]
    }), 200

@bp.route('/lancamentos', methods=['POST'])
@jwt_required()
def criar_lancamento():
    data = request.get_json()
    
    lancamento = Financeiro(
        tipo=data['tipo'],
        categoria=data['categoria'],
        descricao=data['descricao'],
        valor=data['valor'],
        data_vencimento=datetime.fromisoformat(data['data_vencimento']),
        forma_pagamento=data.get('forma_pagamento')
    )
    
    db.session.add(lancamento)
    db.session.commit()
    
    return jsonify({'mensagem': 'Lançamento criado', 'id': lancamento.id}), 201

@bp.route('/fluxo-caixa', methods=['GET'])
@jwt_required()
def fluxo_caixa():
    """Resumo do fluxo de caixa"""
    hoje = datetime.now().date()
    inicio_mes = hoje.replace(day=1)
    
    # Receitas do mês
    receitas = db.session.query(func.sum(Financeiro.valor)).filter(
        Financeiro.tipo == 'receita',
        Financeiro.data_pagamento >= inicio_mes,
        Financeiro.status == 'pago'
    ).scalar() or 0
    
    # Despesas do mês
    despesas = db.session.query(func.sum(Financeiro.valor)).filter(
        Financeiro.tipo == 'despesa',
        Financeiro.data_pagamento >= inicio_mes,
        Financeiro.status == 'pago'
    ).scalar() or 0
    
    # Contas a receber
    a_receber = db.session.query(func.sum(Financeiro.valor)).filter(
        Financeiro.tipo == 'receita',
        Financeiro.status == 'pendente'
    ).scalar() or 0
    
    # Contas a pagar
    a_pagar = db.session.query(func.sum(Financeiro.valor)).filter(
        Financeiro.tipo == 'despesa',
        Financeiro.status == 'pendente'
    ).scalar() or 0
    
    return jsonify({
        'receitas_mes': float(receitas),
        'despesas_mes': float(despesas),
        'saldo_mes': float(receitas - despesas),
        'contas_receber': float(a_receber),
        'contas_pagar': float(a_pagar)
    }), 200
