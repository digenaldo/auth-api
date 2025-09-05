# Importa a extensão SQLAlchemy, usada para integrar o banco de dados ao Flask
# permitindo criar modelos (classes) que viram tabelas.
from flask_sqlalchemy import SQLAlchemy

# Importa a extensão Flask-Migrate, que gerencia migrações do banco de dados
# (alterações de tabelas, colunas, etc. sem precisar recriar tudo).
from flask_migrate import Migrate

# Importa a extensão JWTManager, usada para gerenciar autenticação com tokens JWT.
from flask_jwt_extended import JWTManager


# Cria instâncias das extensões (ainda não ligadas ao app Flask).
db = SQLAlchemy()   # Banco de dados ORM
migrate = Migrate() # Migrações do banco
jwt = JWTManager()  # Gerenciador de tokens JWT


# Função que inicializa as extensões dentro do app Flask.
def init_extensions(app):
    # Inicializa o banco de dados com a aplicação.
    db.init_app(app)
    
    # Inicializa o gerenciador de migrações, ligado ao banco.
    migrate.init_app(app, db)
    
    # Inicializa o sistema de autenticação JWT.
    jwt.init_app(app)
