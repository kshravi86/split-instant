import pytest
import json
from app import app, db
from app.models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def _get_auth_token(client):
    # Signup
    client.post('/api/auth/signup', data=json.dumps({
        'name': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    }), content_type='application/json')

    # Login
    res = client.post('/api/auth/login', data=json.dumps({
        'email': 'test@example.com',
        'password': 'password'
    }), content_type='application/json')
    return json.loads(res.data)['access_token']

def test_signup_and_login(client):
    # Signup
    res = client.post('/api/auth/signup', data=json.dumps({
        'name': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    }), content_type='application/json')
    assert res.status_code == 201
    assert 'access_token' in json.loads(res.data)

    # Login
    res = client.post('/api/auth/login', data=json.dumps({
        'email': 'test@example.com',
        'password': 'password'
    }), content_type='application/json')
    assert res.status_code == 200
    assert 'access_token' in json.loads(res.data)

def test_create_and_get_groups(client):
    token = _get_auth_token(client)
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Create another user to be a participant
    with app.app_context():
        user2 = User(name='participant', email='participant@example.com')
        user2.set_password('password')
        db.session.add(user2)
        db.session.commit()
        participant_id = user2.id

    # Create group
    res = client.post('/api/groups', data=json.dumps({
        'name': 'Test Group',
        'participant_ids': [participant_id]
    }), content_type='application/json', headers=headers)
    print(res.data)
    assert res.status_code == 201

    # Get groups
    res = client.get('/api/groups', headers=headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert len(data) == 1
    assert data[0]['name'] == 'Test Group'

def test_add_and_get_expenses(client):
    token = _get_auth_token(client)
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Create group
    res = client.post('/api/groups', data=json.dumps({
        'name': 'Test Group',
        'participant_ids': []
    }), content_type='application/json', headers=headers)
    print(res.data)
    assert res.status_code == 201

    # Get group id
    res = client.get('/api/groups', headers=headers)
    group_id = json.loads(res.data)[0]['id']

    # Add expense
    res = client.post(f'/api/groups/{group_id}/expenses', data=json.dumps({
        'title': 'Test Expense',
        'amount': 100.00
    }), content_type='application/json', headers=headers)
    assert res.status_code == 201
    assert 'Expense added successfully' in json.loads(res.data)['message']

    # Get expenses
    res = client.get(f'/api/groups/{group_id}/expenses', headers=headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert len(data) == 1
    assert data[0]['title'] == 'Test Expense'

def test_add_settlement(client):
    token = _get_auth_token(client)
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Create another user
    with app.app_context():
        user2 = User(name='testuser2', email='test2@example.com')
        user2.set_password('password')
        db.session.add(user2)
        db.session.commit()
        user2_id = user2.id

    # Create group
    res = client.post('/api/groups', data=json.dumps({
        'name': 'Test Group',
        'participant_ids': [user2_id]
    }), content_type='application/json', headers=headers)
    print(res.data)
    assert res.status_code == 201

    # Get group id
    res = client.get('/api/groups', headers=headers)
    group_id = json.loads(res.data)[0]['id']

    # Add settlement
    res = client.post(f'/api/groups/{group_id}/settlements', data=json.dumps({
        'to_user_id': user2_id,
        'amount': 50.00
    }), content_type='application/json', headers=headers)
    assert res.status_code == 201
    assert 'Settlement recorded successfully' in json.loads(res.data)['message']
