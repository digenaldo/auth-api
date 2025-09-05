# Importa a biblioteca os para acessar variáveis de ambiente e manipular caminhos de arquivos.
import os

# BASE_DIR guarda o caminho absoluto da pasta onde está este arquivo.
# Serve como referência para criar o banco SQLite dentro do projeto.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Classe de configuração da aplicação Flask.
class Config:
    # Chave secreta usada pelo Flask e pelo JWT para assinar cookies e tokens.
    # Primeiro tenta pegar da variável de ambiente SECRET_KEY.
    # Se não existir, usa "dev-secret" (NUNCA usar em produção).
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

    # Define a URL de conexão com o banco de dados.
    # Primeiro tenta pegar da variável DATABASE_URL.
    # Se não existir, usa SQLite como padrão (app.db dentro do projeto).
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    )

    # Desativa rastreamento extra de modificações no SQLAlchemy (economiza memória).
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Define que os tokens JWT só serão buscados nos cabeçalhos HTTP.
    JWT_TOKEN_LOCATION = ["headers"]

    # Tempo de expiração dos tokens JWT → aqui: 24h (60 seg * 60 min * 24 horas).
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24  # 24h

    # Conjunto de API Keys válidas.
    # Lê da variável de ambiente API_KEYS (chaves separadas por vírgula).
    # Se não existir, usa "dev-key" como padrão.
    API_KEYS = set(k.strip() for k in os.environ.get("API_KEYS", "dev-key").split(","))

    # Nome do cabeçalho onde a API Key deve ser enviada.
    # Exemplo: "X-API-Key: dev-key"
    API_KEY_HEADER = os.environ.get("API_KEY_HEADER", "X-API-Key")
