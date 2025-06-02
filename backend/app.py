from flask import Flask, jsonify
from config import Config
from extensions import db, bcrypt, cors
from routes import register_routes
import os
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa extensões
    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # ajuste frontend origin

    register_routes(app)

    # Logging básico
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    with app.app_context():
        db_path = os.path.join(os.path.dirname(__file__), 'finance.db')
        if not os.path.exists(db_path):
            db.create_all()
            logger.info("Banco de dados criado com sucesso.")
        else:
            logger.info("Banco de dados já existe.")

    # Erro genérico para 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Recurso não encontrado"}), 404

    # Erro genérico para 500
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Erro interno do servidor"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    debug_mode = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(debug=debug_mode)
