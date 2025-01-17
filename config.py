class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost/skincare"
    SECRET_KEY = "super secret key"

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "hartaticpg@gmail.com"
    MAIL_PASSWORD = "gpzi zzvd jebq ordv"
    MAIL_DEFAULT_SENDER = "hartaticpg@gmail.com"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
