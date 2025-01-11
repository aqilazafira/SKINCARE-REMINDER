import sqlalchemy as sa


# from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

# bg_schedules = BackgroundScheduler()
# bg_schedules.start()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/skincare"
    app.config["SECRET_KEY"] = "super secret key"

    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "hartaticpg@gmail.com"
    app.config["MAIL_PASSWORD"] = "gpzi zzvd jebq ordv"
    app.config["MAIL_DEFAULT_SENDER"] = "hartaticpg@gmail.com"

    initialize_extensions(app)
    register_blueprints(app)

    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            pirnt("Initialized the database!")

    return app

def initialize_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    mail.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def register_blueprints(app):
    from app.routes.main import main_bp
    from app.routes.user import user_bp
    from app.routes.reminder import reminder_bp
    from app.routes.rekomendasi import rekomendasi_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(reminder_bp)
    app.register_blueprint(rekomendasi_bp)
