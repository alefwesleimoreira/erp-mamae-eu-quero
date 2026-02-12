from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Fornecedor

bp = Blueprint('fornecedores', __name__, url_prefix='/api/fornecedores')

@bp.route('/', methods=['GET'])
@jwt_required()
def listar_fornecedores():
    fornecedores = Fornecedor.query.filter_by(ativo=True).all()
    
    return jsonify({
        'fornecedores': [{
            'id': f.id,
            'razao_social': f.razao_social,
            'nome_fantasia': f.nome_fantasia,
            'cnpj': f.cnpj,
            'telefone': f.telefone
        } for f in fornecedores]
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def criar_fornecedor():
    data = request.get_json()
    
    fornecedor = Fornecedor(
        razao_social=data['razao_social'],
        nome_fantasia=data.get('nome_fantasia'),
        cnpj=data.get('cnpj'),
        email=data.get('email'),
        telefone=data.get('telefone')
    )
    
    db.session.add(fornecedor)
    db.session.commit()
    
    return jsonify({'mensagem': 'Fornecedor criado', 'id': fornecedor.id}), 201
