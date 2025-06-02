from flask import Blueprint, request, jsonify
from models import db, User
from schemas import UserSchema
from sqlalchemy.exc import IntegrityError

users_bp = Blueprint('users', __name__)
user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

@users_bp.route('', methods=['POST'])
def create_user():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Dados não informados"}), 400

    try:
        data = user_schema.load(json_data)
    except Exception as err:
        return jsonify({"error": err.messages}), 422

    user = User(**data)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email já cadastrado"}), 400

    return user_schema.dump(user), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Dados não informados"}), 400

    try:
        data = user_schema.load(json_data, partial=True)
    except Exception as err:
        return jsonify({"error": err.messages}), 422

    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email já cadastrado"}), 400

    return user_schema.dump(user)

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user_schema.dump(user)

@users_bp.route('', methods=['GET'])
def list_users():
    users = User.query.all()
    return user_list_schema.dump(users)
