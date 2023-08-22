import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = BASE_DIR / '.env'
load_dotenv(dotenv_path)


## CONFIG VARIABLES

# Secrey key
SECRET_KEY = os.getenv('SECRET_KEY')

# DB Conf
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Token Conf 
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_REFRESH_SECRET = os.getenv('JWT_REFRESH_SECRET')
HASH_ALGORITHM = os.getenv('HASH_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # 1 hour
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

# Allowed E-mail Domains
ALLOWED_EMAIL_DOMAINS = os.getenv('ALLOWED_EMAIL_DOMAINS').split(' ')


# Debug
DEBUG = True