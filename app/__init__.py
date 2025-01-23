import os
import sqlalchemy as sa
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

scheduler = BackgroundScheduler()


def create_app():
    app = Flask(__name__)
    config_type = os.getenv("APP_SETTING", default="config.Config")
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    register_cli_commands(app)

    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("Initialized the database!")

    return app


def initialize_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    mail.init_app(app)

    scheduler.app = app

    if not app.config["TESTING"]:
        scheduler.start()

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def register_blueprints(app):
    from app.routes.admin import admin_bp
    from app.routes.main import main_bp
    from app.routes.rekomendasi import rekomendasi_bp
    from app.routes.reminder import reminder_bp
    from app.routes.user import user_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(reminder_bp)
    app.register_blueprint(rekomendasi_bp)
    app.register_blueprint(admin_bp)


def register_cli_commands(app):
    from app.seed import seed_data

    @app.cli.command("init-db")
    def init_db():
        with app.app_context():
            db.create_all()
            seed_data()

    @app.cli.command("reset-db")
    def reset_db():
        with app.app_context():
            db.drop_all()
