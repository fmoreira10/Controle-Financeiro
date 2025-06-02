from flask import Blueprint, jsonify, request
from models import db, Category, TypeEnum

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    result = [category.to_dict() for category in categories]
    return jsonify(result)

@categories_bp.route('/', methods=['POST'])
def create_category():
    data = request.json
    try:
        category = Category(
            name=data['name'],
            type=TypeEnum(data['type']),
            description=data.get('description', '')
        )
        db.session.add(category)
        db.session.commit()
        return jsonify({"message": "Categoria criada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.json
    try:
        category.name = data['name']
        category.type = TypeEnum(data['type'])
        category.description = data.get('description', category.description)
        db.session.commit()
        return jsonify({"message": "Categoria atualizada com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Categoria deletada com sucesso!"})
