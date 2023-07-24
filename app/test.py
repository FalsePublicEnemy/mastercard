import pytest
import json
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def cleanup_on_teardown():
    # Add this function to flush db on every test and be
    # able to use same email twice
    from app.main import database
    database.clear()

def test_healthcheck():
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json() == {'message': 'Server is running'}


def test_create_account():
    data = {
        'name': 'Karim Nassar',
        'email': 'karimnassar2012@gmail.com',
        'balance': 100,
        'active': False,
        'description': 'Hello'
    }
    response = client.post('/api/accounts', json=data)
    assert response.status_code == 201

    response = response.json()['result']
    response.pop('id')
    assert response == data

    cleanup_on_teardown()


@pytest.mark.parametrize(
    'data',
    [
        (
            {
                'name': 123,
                'email': 'karimnassar2012@gmail.com',
                'balance': 100,
                'active': False,
                'description': 'Hello',
            },
        ),
        ( 
            {
                'name': 'Not me',
                'email': 'karim@gmail.com',
                'balance': 'NOT A FLOAT',
                'active': False,
                'description': 'Hello',
            }
        )
    ]
)
def test_create_account_bad_request(data):
    response = client.post('/api/accounts', json=data)
    assert response.status_code == 422
    cleanup_on_teardown()


@pytest.mark.parametrize(
    'data',
    [
        (
            {
                'name': 'Karim Nassar',
                'email': 'karimnassar2012@gmail.com',
                'balance': 100,
                'active': False,
                'description': 'Hello',
            }, 
            {
                'name': 'Not me',
                'email': 'karim@gmail.com',
                'balance': 100,
                'active': False,
                'description': 'Hello',
            }
        )
    ]
)
def test_list_account(data):
    response = client.post('/api/accounts', json=data[0])
    assert response.status_code == 201

    response = client.post('/api/accounts', json=data[1])
    assert response.status_code == 201

    response = client.get('/api/accounts')
    assert response.status_code == 200

    response = response.json()
    assert list(response.values()) == list(data)
    cleanup_on_teardown()


def test_delete_account():
    data = {
        'name': 'Karim Nassar',
        'email': 'karimnassar2012@gmail.com',
        'balance': 100,
        'active': False,
        'description': 'Hello'
    }
    response = client.post('/api/accounts', json=data)
    assert response.status_code == 201

    response = response.json()['result']
    account_id = response.pop('id')
    assert response == data

    response = client.delete(f'/api/accounts/{account_id}')
    assert response.status_code == 200

    response = client.get(f'/api/accounts/{account_id}')
    assert response.status_code == 404
