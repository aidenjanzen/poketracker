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

def test_database():
    pass

# ----------------------------------------------------------- tests for login -------------------------------------------------------

@pytest.fixture
def client():
    return app.test_client()

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

# def test_login_incorrect_password(client):
#     with client:
#         response = client.post('/login', data={'username': 'mpt', 'password': 'incorrect'}, follow_redirects=True)
#         print(response.data)
#         assert response.status_code == 200  # Check if redirected after incorrect password
#         assert b'Incorrect password.' in response.data  # Check if flash message present

# def test_already_logged_in(client):
#     with client:
#         response = client.post('/login', data={'username': 'mpt', 'password': '123'}, follow_redirects=True)
#         print(response.data)
#         assert response.status_code == 302  # Check if redirected after successful login

#         # Attempt to log in again
#         response = client.post('/login', data={'username': 'mpt', 'password': '123'}, follow_redirects=True)
#         assert response.status_code == 200  # Check if redirected
#         assert b'Already logged in.' in response.data  # Check if flash message present



# ----------------------------------------------------------- tests for register -------------------------------------------------------