from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()
jwt = JWTManager()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
cache = Cache()

