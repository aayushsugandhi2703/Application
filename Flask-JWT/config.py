from secret import get_secret_key

class Config:
    SECRET_KEY = get_secret_key()
    JWT_SECRET_KEY = get_secret_key()
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
