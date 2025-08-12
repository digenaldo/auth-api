from flask import Flask, jsonify
from .extensions import init_extensions
from .routes.users import bp as users_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    init_extensions(app)

    @app.get("/")
    def health():
        return jsonify({"status": "ok"})

    app.register_blueprint(users_bp)
    return app
