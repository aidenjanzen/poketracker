from app import app
from models import Users, Pokemon, PokeCollection, Collection
from database import db
import pytest
from pokedex import pokedex

def test_connection():
    response = app.test_client().get('/')
    assert response.status_code == 200

def test_user():
    user = Users
    user.username = "Noah Test"
    user.password = "badpassword"
    assert isinstance(user.username, str)
    assert isinstance(user.password, str)

def test_pokemon():
    pokemon = Pokemon
    pokemon.number = 6
    assert pokedex[pokemon.number]["name"] == "Charizard"
    assert "Fire" in pokedex[pokemon.number]["type"]

def test_collection(): #not sure how but should create a user, foreign key that user to the collection and call collection for its id
    collection = Collection
    
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.app_context():
        db.create_all()  # Create tables for testing
        yield app.test_client()
        db.drop_all()  # Clean up / drop tables after test

def test_database(client):
    with app.app_context():  # Ensure app context is available
        db.drop_all()
        db.create_all()
        user = Users(username="mpt", password="123")
        db.session.add(user)
        db.session.commit()

# ----------------------------------------------------------- tests for routes -------------------------------------------------------

def test_base(client):
    response = client.get('/')
    assert response.status_code == 200

def test_home(client):
    response = client.get('/home')
    assert response.status_code == 200

def test_gen(client):
    number = 1
    response = client.get(f'/gen{number}')
    assert response.status_code == 200
    assert b'Generation 1' in response.data
    assert b'1' in response.data  # Check if it includes start number

    number = 5
    response = client.get(f'/gen{number}')
    assert response.status_code == 200
    assert b'Generation 5' in response.data
    assert b'5' in response.data  # Check if it includes start number

    number = 9
    response = client.get(f'/gen{number}')
    assert response.status_code == 200
    assert b'Generation 9' in response.data
    assert b'9' in response.data  # Check if it includes start number

# ----------------------------------------------------------- tests for login -------------------------------------------------------

def test_login_successful(client):
    with client:
        response = client.post('/login', data={'username': 'mpt', 'password': '123'}, follow_redirects=True)
        assert response.status_code == 200  # Check if redirected after successful login
        assert b'Already logged in.' not in response.data  # Check if flash message not present

def test_login_missing_username(client):
    with client:
        response = client.post('/login', data={'username': '', 'password': '123'}, follow_redirects=True)
        assert response.status_code == 200  # Check if redirected after missing username
        assert b'Please enter a username.' in response.data  # Check if flash message present

def test_login_nonexistent_user(client):
    with client:
        response = client.post('/login', data={'username': 'nonexistent', 'password': '123'}, follow_redirects=True)
        assert response.status_code == 200  # Check if redirected after nonexistent user
        assert b'No user found.' in response.data  # Check if flash message present

# def test_login_incorrect_password(client): #haven't got this working yet
#     with client:
#         response = client.post('/login', data={'username': 'mpt', 'password': 'incorrect'}, follow_redirects=True)
#         print(response.data)
#         assert response.status_code == 200  # Check if redirected after incorrect password
#         assert b'Incorrect password.' in response.data  # Check if flash message present

# def test_already_logged_in(client): #haven't got this working yet
#     with client:
#         response = client.post('/login', data={'username': 'mpt', 'password': '123'}, follow_redirects=True)
#         print(response.data)
#         assert response.status_code == 302  # Check if redirected after successful login

#         # Attempt to log in again
#         response = client.post('/login', data={'username': 'mpt', 'password': '123'}, follow_redirects=True)
#         assert response.status_code == 200  # Check if redirected
#         assert b'Already logged in.' in response.data  # Check if flash message present

# ----------------------------------------------------------- tests for register -------------------------------------------------------

def test_register_successful(client):
    with client:
        response = client.post('/register', data={'username': 'testuser', 'password': 'test'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"User already exists, please login." not in response.data

def test_register_missing_username(client):
    with client:
        response = client.post('/register', data={'username': '', 'password': '123'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Please enter a username.' in response.data

def test_register_missing_password(client):
    with client:
        response = client.post('/register', data={'username': 'testuser', 'password': ''}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Please enter a password.' in response.data

# def test_register_user_exists(client): #haven't got this working yet
#     with client:
#         response = client.post('/register', data={'username': 'mpt', 'password': '123'}, follow_redirects=True)
#         assert response.status_code == 200
#         print(response.data)
#         assert b"User already exists, please login." in response.data

# ----------------------------------------------------------- tests for add and remove and collections and logout-------------------------------------------------------
def test_add_pokemon(client):
    with client: 
        response = client.post('/add', follow_redirects=True) #check if not logged in
        assert response.status_code == 200
        assert b'You are not logged in.' in response.data
def test_remove_pokemon(client):
    with client: 
        response = client.post('/remove', follow_redirects=True) #check if not logged in
        assert response.status_code == 200
        assert b'You are not logged in.' in response.data
def test_collection(client):
    with client: 
        response = client.get('/collections', follow_redirects=True) #check if not logged in
        assert response.status_code == 200
        assert b'You are not logged in.' in response.data
def test_logout(client):
    with client: 
        response = client.get('/logout', follow_redirects=True) #check if not logged in
        assert response.status_code == 200