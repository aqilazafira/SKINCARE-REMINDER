import os

from dotenv import load_dotenv

if os.getenv("FLASK_ENV") != "production":
    load_dotenv()

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root@localhost/skincare2")
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "reminderskincare@gmail.com"
    MAIL_PASSWORD = "bgvw qfsn rspq cvsm"
    MAIL_DEFAULT_SENDER = "reminderskincare@gmail.com"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
