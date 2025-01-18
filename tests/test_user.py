from app.models import User


def test_user_registration(client, init_db):
    response = client.post(
        "/register",
        data=dict(username="newuser", email="newuser@example.com", password="password", confirm_password="password"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    user = User.query.filter_by(username="newuser").first()
    assert user is not None


def test_user_login(client, init_db):
    response = client.post("/login", data=dict(username="testuser1", password="password"), follow_redirects=True)
    assert response.status_code == 200
    assert b"Home" in response.data


def test_user_logout(auth_client, init_db):
    response = auth_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
