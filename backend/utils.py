from extensions import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(password_hash: str, password: str) -> bool:
    return bcrypt.check_password_hash(password_hash, password)

def generate_token(user_id: int) -> str:
    return jwt.encode({'user_id': user_id}, Config.SECRET_KEY, algorithm='HS256')

def verify_token(token: str) -> int:
    return jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])

def send_email(to: str, subject: str, body: str):
    msg = Message(subject, recipients=[to], body=body)
    mail.send(msg)

def generate_password_reset_token(email: str) -> str:
    return jwt.encode({'email': email}, Config.SECRET_KEY, algorithm='HS256')

def verify_password_reset_token(token: str) -> str:
    return jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
    


