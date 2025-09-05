# Importa a classe principal Flask (para criar a aplicação web)
# e jsonify (para devolver respostas no formato JSON).
from flask import Flask, jsonify

# Importa a função que inicializa extensões (ex.: banco de dados, JWT etc.).
from .extensions import init_extensions

# Importa o blueprint de usuários (conjunto de rotas relacionadas a "users").
# Aqui damos o apelido "users_bp" para usar depois.
from .routes.users import bp as users_bp

# Importa o decorator que exige o uso de API Key em algumas rotas.
from .security import require_api_key


# Função de fábrica que cria e configura a aplicação Flask.
def create_app():
    # Cria a instância principal do Flask.
    app = Flask(__name__)
    
    # Carrega as configurações da aplicação a partir da classe Config (arquivo config.py).
    app.config.from_object("config.Config")
    
    # Inicializa extensões (ex.: conexão com o banco, JWT, etc.).
    init_extensions(app)

    # ------------------------
    # Rota de "saúde" (health check)
    # ------------------------
    @app.get("/")        # Define rota GET em "/"
    @require_api_key     # Exige API Key para acessar
    def health():
        # Retorna um JSON simples indicando que a aplicação está funcionando.
        return jsonify({"status": "ok"})

    # Registra o blueprint de usuários na aplicação (rotas /users, /users/login, etc.).
    app.register_blueprint(users_bp)
    
    # Retorna a aplicação configurada.
    return app
