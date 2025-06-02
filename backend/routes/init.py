from flask import Blueprint

def register_routes(app):
    from .users import users_bp
    from .transactions import transactions_bp
    from .categories import categories_bp

    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
