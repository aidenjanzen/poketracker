from app import app

def test_connection():
    response = app.test_client().get('/')
    assert response.status_code == 200