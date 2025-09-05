# Importa datetime para registrar a data/hora de criação do usuário.
from datetime import datetime

# Importa o objeto db, que representa o banco de dados (ORM do SQLAlchemy).
from .extensions import db


# Define a classe User, que representa a tabela "users" no banco de dados.
class User(db.Model):
    # Define o nome da tabela no banco explicitamente como "users".
    __tablename__ = "users"

    # Coluna "id": número inteiro, chave primária (identificador único de cada usuário).
    id = db.Column(db.Integer, primary_key=True)

    # Coluna "email": string de até 255 caracteres.
    # unique=True → não pode haver dois usuários com o mesmo email.
    # nullable=False → campo obrigatório (não pode ser nulo).
    # index=True → cria um índice no banco para buscas mais rápidas por email.
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)

    # Coluna "password_hash": string de até 255 caracteres, obrigatória.
    # Aqui armazenamos a senha criptografada (nunca em texto puro!).
    password_hash = db.Column(db.String(255), nullable=False)

    # Coluna "created_at": armazena a data e hora em que o usuário foi criado.
    # default=datetime.utcnow → o valor padrão será o momento da criação.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
