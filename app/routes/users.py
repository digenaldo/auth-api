# Importa o Blueprint (para organizar rotas), request (para pegar dados da requisição)
# e jsonify (para devolver respostas em formato JSON).
from flask import Blueprint, request, jsonify

# Importa o modelo User (representa a tabela de usuários no banco).
from ..models import User

# Importa funções de autenticação e criação de usuário.
from ..auth.service import create_user, authenticate

# Importa o decorator jwt_required (exige login para acessar rota)
# e get_jwt_identity (recupera o usuário logado pelo token).
from flask_jwt_extended import jwt_required, get_jwt_identity

# Importa a função personalizada que valida o uso de API Key.
from ..security import require_api_key


# Cria um Blueprint chamado "users", com as rotas começando por /users.
bp = Blueprint("users", __name__, url_prefix="/users")


# ---------------------------
# Rota de REGISTRO de usuários
# ---------------------------
@bp.post("")          # Define que essa função responde a requisições POST em /users
@require_api_key      # Exige que seja enviada uma API Key válida para usar essa rota
def register():
    # Pega os dados enviados em JSON na requisição (ou um dicionário vazio).
    data = request.get_json() or {}
    email = data.get("email")       # Extrai o campo "email"
    password = data.get("password") # Extrai o campo "password"
    
    # Se não recebeu email ou senha, retorna erro 400 (Bad Request).
    if not email or not password:
        return jsonify({"error": "email e password são obrigatórios"}), 400
    
    # Verifica se já existe um usuário com esse email no banco.
    if User.query.filter_by(email=email).first():
        # Se já existir, retorna erro 409 (Conflict).
        return jsonify({"error": "email já cadastrado"}), 409
    
    # Cria um novo usuário no banco (senha é salva criptografada).
    user = create_user(email, password)
    
    # Retorna os dados do usuário criado e status 201 (Created).
    return jsonify({"id": user.id, "email": user.email}), 201


# ----------------------
# Rota de LOGIN de usuário
# ----------------------
@bp.post("/login")  # Define que essa função responde a POST em /users/login
def login():
    # Pega os dados enviados na requisição (ou vazio).
    data = request.get_json() or {}
    
    # Chama a função authenticate passando email e senha (ou "" se não veio nada).
    token = authenticate(data.get("email",""), data.get("password",""))
    
    # Se não gerou token (credenciais erradas), retorna erro 401 (Unauthorized).
    if not token:
        return jsonify({"error": "credenciais inválidas"}), 401
    
    # Se deu certo, retorna o token JWT.
    return jsonify({"access_token": token})


# ----------------------
# Rota de LISTAR usuários
# ----------------------
@bp.get("")          # Define que essa função responde a GET em /users
@jwt_required()      # Exige que o usuário esteja logado (enviar JWT válido)
def list_users():
    # Recupera a identidade do usuário logado (aqui não usamos, mas poderia).
    _ = get_jwt_identity()
    
    # Busca todos os usuários no banco, mas apenas os campos id e email.
    users = User.query.with_entities(User.id, User.email).all()
    
    # Monta e devolve um JSON com a lista de usuários.
    return jsonify([{"id": u.id, "email": u.email} for u in users])
