import os
import pytest
from flask_login import FlaskLoginClient

from app import create_app, db
from app.models import Reminder, SkincareType, User, Product
from app.seed import seed_data


@pytest.fixture()
def app():
    os.environ["APP_SETTING"] = "config.TestingConfig"

    app = create_app()
    app.test_client_class = FlaskLoginClient
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def init_db(app):
    with app.app_context():
        db.create_all()

        user1 = User(username="testuser1", email="testuser1@example.com", role="admin")
        user1.set_password("password")
        db.session.add(user1)
        db.session.commit()

        user2 = User(username="testuser2", email="testuser2@example.com")
        user2.set_password("password")
        db.session.add(user2)
        db.session.commit()

        product = Product(brand="Test Brand", description="Test Description", image_url="test.jpg")
        db.session.add(product)
        db.session.commit()

        seed_data()

        yield

        db.drop_all()


@pytest.fixture(scope="function")
def auth_client(app, init_db):
    user = User.query.get(1)
    with app.test_client(user=user) as client:
        yield client


@pytest.fixture(scope="function")
def test_user(app, init_db):
    user = User.query.get(1)
    return user
