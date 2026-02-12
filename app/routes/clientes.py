from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Cliente

bp = Blueprint('clientes', __name__, url_prefix='/api/clientes')

@bp.route('/', methods=['GET'])
@jwt_required()
def listar_clientes():
    page = request.args.get('page', 1, type=int)
    busca = request.args.get('q')
    
    query = Cliente.query
    if busca:
        query = query.filter(
            db.or_(
                Cliente.nome.ilike(f'%{busca}%'),
                Cliente.email.ilike(f'%{busca}%'),
                Cliente.cpf.ilike(f'%{busca}%')
            )
        )
    
    clientes = query.paginate(page=page, per_page=50, error_out=False)
    
    return jsonify({
        'clientes': [{
            'id': c.id,
            'nome': c.nome,
            'email': c.email,
            'telefone': c.telefone,
            'cidade': c.cidade
        } for c in clientes.items],
        'total': clientes.total
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def criar_cliente():
    data = request.get_json()
    
    cliente = Cliente(
        nome=data['nome'],
        cpf=data.get('cpf'),
        email=data.get('email'),
        telefone=data.get('telefone'),
        cep=data.get('cep'),
        logradouro=data.get('logradouro'),
        numero=data.get('numero'),
        bairro=data.get('bairro'),
        cidade=data.get('cidade'),
        estado=data.get('estado')
    )
    
    db.session.add(cliente)
    db.session.commit()
    
    return jsonify({'mensagem': 'Cliente criado', 'id': cliente.id}), 201

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    return jsonify({
        'id': cliente.id,
        'nome': cliente.nome,
        'cpf': cliente.cpf,
        'email': cliente.email,
        'telefone': cliente.telefone,
        'endereco': {
            'cep': cliente.cep,
            'logradouro': cliente.logradouro,
            'numero': cliente.numero,
            'bairro': cliente.bairro,
            'cidade': cliente.cidade,
            'estado': cliente.estado
        }
    }), 200
