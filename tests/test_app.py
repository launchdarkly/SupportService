import sys
import os
import tempfile
import pytest 

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path + '/../')

from app import app

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_index(client):
    response = client.get('/')
    assert b'title' in response.data