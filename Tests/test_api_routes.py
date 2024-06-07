import pytest
from servidor import create_app, db_session
from servidor.database import init_db

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        init_db(app)
    yield app
    with app.app_context():
        db_session.remove()

@pytest.fixture
def client(app):
    return app.test_client()

def test_ping(client):
    """Test the /api/ping route."""
    response = client.get('/api/ping')
    assert response.status_code == 200
    assert response.json == {'message': 'pong'}
