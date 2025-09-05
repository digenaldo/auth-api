# Importa a biblioteca bcrypt, usada para gerar e verificar senhas criptografadas.
import bcrypt

# Importa a função para criar tokens JWT (usada para autenticação baseada em token).
from flask_jwt_extended import create_access_token

# Importa o modelo User (representa a tabela de usuários no banco de dados).
from ..models import User

# Importa o objeto db (conexão e controle do banco de dados).
from ..extensions import db


# Função que recebe uma senha em texto puro e devolve ela criptografada.
def hash_password(plain: str) -> str:
    # bcrypt.hashpw() gera o hash da senha com um "sal" aleatório.
    # .encode() transforma a string em bytes, pois o bcrypt só trabalha com bytes.
    # .decode() transforma o hash (que é bytes) de volta para string.
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


# Função que verifica se a senha digitada bate com o hash armazenado no banco.
def check_password(plain: str, hashed: str) -> bool:
    # bcrypt.checkpw() compara a senha digitada (em bytes) com o hash (em bytes).
    return bcrypt.checkpw(plain.encode(), hashed.encode())


# Função para criar um novo usuário no banco de dados.
def create_user(email: str, password: str) -> User:
    # Cria um objeto User, já salvando a senha em formato criptografado.
    user = User(email=email, password_hash=hash_password(password))
    
    # Adiciona o novo usuário na sessão do banco (pendente de commit).
    db.session.add(user)
    
    # Efetiva a gravação no banco de dados (commit).
    db.session.commit()
    
    # Retorna o usuário criado.
    return user


# Função que autentica o usuário (login).
def authenticate(email: str, password: str) -> str | None:
    # Busca no banco o primeiro usuário com o email informado.
    user = User.query.filter_by(email=email).first()
    
    # Se o usuário existe e a senha digitada confere com a senha do banco:
    if user and check_password(password, user.password_hash):
        # Cria um token JWT (com id do usuário como identidade e email como dado extra).
        return create_access_token(
            identity=str(user.id),
            additional_claims={"email": user.email}
        )
    
    # Se não encontrou ou senha não bate, retorna None (falha na autenticação).
    return None
