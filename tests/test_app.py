def test_app_config(app):
    assert not app.config["DEBUG"]
    assert app.config["TESTING"]
    assert "memory" in app.config["SQLALCHEMY_DATABASE_URI"]

def test_home_page(auth_client):
    response = auth_client.get('/')
    assert response.status_code == 200
    assert b"SKINCARE REMINDER" in response.data
