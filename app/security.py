# Importa wraps (para preservar metadados da função decorada),
# current_app (acessa a configuração do Flask atual),
# request (para pegar dados da requisição)
# e jsonify (para retornar respostas em JSON).
from functools import wraps
from flask import current_app, request, jsonify


# Função que cria um decorator para exigir API Key em rotas específicas.
def require_api_key(fn):
    # @wraps(fn) → mantém o nome e docstring da função original.
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Pega do config o nome do cabeçalho onde a chave deve estar.
        # Ex.: "X-API-KEY".
        header_name = current_app.config["API_KEY_HEADER"]

        # Busca a API Key enviada no cabeçalho da requisição.
        api_key = request.headers.get(header_name)

        # Se não existir ou não estiver na lista de chaves válidas da config → erro 401.
        if not api_key or api_key not in current_app.config["API_KEYS"]:
            return jsonify({"error": "invalid or missing API key"}), 401

        # Se a chave for válida, executa a função original normalmente.
        return fn(*args, **kwargs)

    # Retorna a função decorada.
    return wrapper
