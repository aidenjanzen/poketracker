from app import app
from models import Users

def test_connection():
    response = app.test_client().get('/')
    assert response.status_code == 200

def test_user():
    user = Users
    user.username = "Noah Test"
    user.password = "badpassword"
    assert isinstance(user.username, str)
    assert isinstance(user.password, str)