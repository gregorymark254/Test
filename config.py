import os
from datetime import timedelta

from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_TOKEN_LOCATION = ['headers']
JWT_IDENTITY_CLAIM = 'user_id'
JWT_ACCESS_TOKEN_EXPIRED = timedelta(hours=3)
CACHE_TYPE = 'RedisCache'
