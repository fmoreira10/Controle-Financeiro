from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager  # ✅ ADICIONE ESTA LINHA

db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()
jwt = JWTManager()


