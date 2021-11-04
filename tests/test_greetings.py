import json
import os
import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app({ 'TESTING': True })

    with app.test_client() as client:
        yield client


def test_greetings(client):
    res = client.get('/api/v1/greetings')
    resp = json.loads(res.data)
    assert resp['hello'] == 'world'
