from flask import Blueprint, jsonify

# Importa blueprints dos módulos
from .users import users_bp
from .categories import categories_bp
from .transactions import transactions_bp

# Blueprint principal para agrupar rotas API
api_bp = Blueprint('api', __name__)

# Rota simples de teste
@api_bp.route('/hello')
def hello():
    return jsonify({"message": "API funcionando!"})

def register_routes(app):
    # Registra blueprints com prefixo
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    
