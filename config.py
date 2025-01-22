class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/skincare"
    SECRET_KEY = "super secret key"

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "reminderskincare@gmail.com"
    MAIL_PASSWORD = "bgvw qfsn rspq cvsm"
    MAIL_DEFAULT_SENDER = "reminderskincare@gmail.com"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
