from flask import Blueprint, jsonify, request
from models import db, Transaction, TypeEnum

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    result = [t.to_dict() for t in transactions]
    return jsonify(result)

@transactions_bp.route('/', methods=['POST'])
def create_transaction():
    data = request.json
    try:
        transaction = Transaction(
            user_id=data['user_id'],
            type=TypeEnum(data['type']),
            value=data['value'],
            category_id=data['category_id'],
            description=data.get('description', ''),
            date=data.get('date', None),
            is_recurring=data.get('is_recurring', False),
            payment_method=data.get('payment_method', 'other'),
            recurring_interval=data.get('recurring_interval', None),
            status=data.get('status', 'completed')
        )
        db.session.add(transaction)
        db.session.commit()
        return jsonify({"message": "Transação criada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@transactions_bp.route('/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    data = request.json
    try:
        transaction.user_id = data['user_id']
        transaction.type = TypeEnum(data['type'])
        transaction.value = data['value']
        transaction.category_id = data['category_id']
        transaction.description = data.get('description', transaction.description)
        transaction.date = data.get('date', transaction.date)
        transaction.is_recurring = data.get('is_recurring', transaction.is_recurring)
        transaction.payment_method = data.get('payment_method', transaction.payment_method)
        transaction.recurring_interval = data.get('recurring_interval', transaction.recurring_interval)
        transaction.status = data.get('status', transaction.status)
        db.session.commit()
        return jsonify({"message": "Transação atualizada com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@transactions_bp.route('/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transação deletada com sucesso!"})
