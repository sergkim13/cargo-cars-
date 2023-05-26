import os

from dotenv import load_dotenv

load_dotenv()

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
INTERVAL_SECONDS = os.environ.get('INTERVAL_SECONDS')

# Database
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
SQLALCHEMY_ECHO = bool(os.environ.get('SQLALCHEMY_ECHO'))
TEST_DB_NAME = os.environ.get('TEST_DB_NAME')

# Cache
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_DB = os.environ.get('REDIS_DB')
REDIS_EXP = os.environ.get('REDIS_EXP')
