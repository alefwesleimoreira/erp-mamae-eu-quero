from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.models import Usuario, Cliente
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Registrar novo usuário/cliente"""
    data = request.get_json()
    
    # Validações
    if not data.get('email') or not data.get('senha'):
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
    
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'erro': 'Email já cadastrado'}), 400
    
    # Criar usuário
    usuario = Usuario(
        nome=data.get('nome'),
        email=data['email'],
        tipo='cliente'
    )
    usuario.set_senha(data['senha'])
    
    db.session.add(usuario)
    db.session.flush()
    
    # Criar cliente associado
    cliente = Cliente(
        usuario_id=usuario.id,
        nome=data.get('nome'),
        email=data['email'],
        telefone=data.get('telefone'),
        cpf=data.get('cpf')
    )
    
    db.session.add(cliente)
    db.session.commit()
    
    # Gerar tokens
    access_token = create_access_token(identity=usuario.id)
    refresh_token = create_refresh_token(identity=usuario.id)
    
    return jsonify({
        'mensagem': 'Usuário criado com sucesso',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'usuario': {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'tipo': usuario.tipo
        }
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    """Login de usuário"""
    data = request.get_json()
    
    if not data.get('email') or not data.get('senha'):
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
    
    usuario = Usuario.query.filter_by(email=data['email']).first()
    
    if not usuario or not usuario.verificar_senha(data['senha']):
        return jsonify({'erro': 'Credenciais inválidas'}), 401
    
    if not usuario.ativo:
        return jsonify({'erro': 'Usuário inativo'}), 403
    
    # Gerar tokens
    access_token = create_access_token(identity=usuario.id)
    refresh_token = create_refresh_token(identity=usuario.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'usuario': {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'tipo': usuario.tipo
        }
    }), 200

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Renovar access token"""
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token}), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """Obter dados do usuário logado"""
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo': usuario.tipo,
        'ativo': usuario.ativo
    }), 200
