from extensions import db
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import validates
import re

class TypeEnum(Enum):
    INCOME = 'income'
    EXPENSE = 'expense'

class PaymentMethodEnum(Enum):
    CASH = 'cash'
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'
    BANK_TRANSFER = 'bank_transfer'
    PIX = 'pix'
    OTHER = 'other'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hashed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade='all, delete-orphan')

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError('Email não pode estar vazio')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError('Email inválido')
        return email.lower()

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 3:
            raise ValueError('Nome deve ter pelo menos 3 caracteres')
        return name.strip()

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum(TypeEnum), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions = db.relationship('Transaction', backref='category', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.Enum(TypeEnum), nullable=False)
    value = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_recurring = db.Column(db.Boolean, default=False)
    payment_method = db.Column(db.Enum(PaymentMethodEnum), nullable=False, default=PaymentMethodEnum.OTHER)
    recurring_interval = db.Column(db.Integer)  # em dias
    status = db.Column(db.String(20), default='completed')

class RecurringTransaction(db.Model):
    __tablename__ = 'recurring_transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    next_occurrence = db.Column(db.DateTime, nullable=False)
    last_occurrence = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    transaction = db.relationship('Transaction', backref='recurring_transaction', lazy=True)
    

    
    
