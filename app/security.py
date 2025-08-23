from functools import wraps
from flask import current_app, request, jsonify

def require_api_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header_name = current_app.config["API_KEY_HEADER"]
        api_key = request.headers.get(header_name)
        if not api_key or api_key not in current_app.config["API_KEYS"]:
            return jsonify({"error": "invalid or missing API key"}), 401
        return fn(*args, **kwargs)
    return wrapper
