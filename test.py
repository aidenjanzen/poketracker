from app import app
from models import Users
from database import db
import pytest

def test_connection():
    response = app.test_client().get('/')
    assert response.status_code == 200

def test_user():
    user = Users
    user.username = "Noah Test"
    user.password = "badpassword"
    assert isinstance(user.username, str)
    assert isinstance(user.password, str)

def test_database():
    pass

@pytest.fixture
def client():
    return app.test_client()

def test_base(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home Page - nogen' in response.data

def test_home(client):
    response = client.get('/home')
    assert response.status_code == 200
    assert b'Home Page - nogen' in response.data

def test_search(client):
    response = client.get('/search')
    assert response.status_code == 200
    assert b'Search Page' in response.data

def test_gen(client):
    number = 1
    response = client.get(f'/gen{number}')
    assert response.status_code == 200
    assert b'Generation 1' in response.data
    assert b'1' in response.data  # Check if it includes start number