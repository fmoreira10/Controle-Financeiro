from marshmallow import Schema, fields, validate, ValidationError, post_load
from models import TypeEnum, PaymentMethodEnum
from utils import hash_password

def must_be_enum(value):
    if value not in [e.value for e in TypeEnum]:
        raise ValidationError(f"Valor inválido: {value}")

def must_be_payment_enum(value):
    if value not in [e.value for e in PaymentMethodEnum]:
        raise ValidationError(f"Valor inválido: {value}")

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    created_at = fields.DateTime(dump_only=True)
    active = fields.Bool(dump_only=True)

    @post_load
    def hash_password(self, data, **kwargs):
        data['password'] = hash_password(data['password'])
        return data

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    type = fields.Str(required=True, validate=must_be_enum)
    description = fields.Str()

class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    type = fields.Str(required=True, validate=must_be_enum)
    value = fields.Float(required=True)
    category_id = fields.Int(required=True)
    description = fields.Str()
    date = fields.DateTime()
    is_recurring = fields.Bool()
    payment_method = fields.Str(validate=must_be_payment_enum)
    recurring_interval = fields.Int()
    status = fields.Str(validate=validate.OneOf(['completed', 'pending', 'cancelled']))

class RecurringTransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    transaction_id = fields.Int(required=True)
    interval = fields.Int(required=True)
    next_occurrence = fields.DateTime(required=True)
    last_occurrence = fields.DateTime()
    is_active = fields.Bool(load_default=True)
    transaction = fields.Nested(TransactionSchema, only=('id', 'type', 'value', 'category_id', 'description', 'date'))

